import discord
from discord.ui import Button, View

"""
This code is a modified version from: 
https://github.com/Pycord-Development/pycord/blob/16f9bcb5f43f614cb2eb7691c978f2e9f28548c8/discord/ext/pages/pagination.py

The original code had some bugs involved, therefore it has been reimplemented - while most of the code has been
reused from the original source, there are modifications implemented by myself.
"""


class Navigator(Button):
    def __init__(self, style, disabled, label, button_type, paginator):
        super().__init__(style=style, disabled=disabled, label=label, row=0)
        self.style = style
        self.disabled = disabled
        self.label = label
        self.button_type = button_type
        self.paginator = paginator

    async def callback(self, interaction: discord.Interaction):
        if self.button_type == "<<":
            self.paginator.current_page = 0
        elif self.button_type == "<":
            self.paginator.current_page -= 1
        elif self.button_type == ">":
            self.paginator.current_page += 1
        elif self.button_type == ">>":
            self.paginator.current_page = self.paginator.page_count
        await self.paginator.navigate(interaction, self.paginator.current_page)


class Paginator(View):
    def __init__(self, author, message, pages, timeout=180.0):
        super().__init__(timeout=timeout)
        self.pages = pages
        self.timeout = timeout
        self.current_page = 0
        self.page_count = len(self.pages) - 1
        self.message = message
        self.buttons = {
            "<<": {
                "object": Navigator(
                    style=discord.ButtonStyle.green,
                    disabled=True,
                    label="<<",
                    button_type="<<",
                    paginator=self,
                )
            },
            "<": {
                "object": Navigator(
                    style=discord.ButtonStyle.green,
                    disabled=True,
                    label="<",
                    button_type="<",
                    paginator=self,
                )
            },
            "page_number": {
                "object": Button(
                    style=discord.ButtonStyle.blurple,
                    disabled=True,
                    label=f"{self.current_page + 1}/{self.page_count + 1}",
                    row=0,
                )
            },
            ">": {
                "object": Navigator(
                    style=discord.ButtonStyle.green,
                    disabled=True,
                    label=">",
                    button_type=">",
                    paginator=self,
                )
            },
            ">>": {
                "object": Navigator(
                    style=discord.ButtonStyle.green,
                    disabled=True,
                    label=">>",
                    button_type=">>",
                    paginator=self,
                )
            },
        }
        self.update_buttons()
        self.user = author

    async def on_timeout(self):
        for button in self.children:
            button.disabled = True
        await self.message.edit(view=self)

    async def navigate(self, interaction: discord.Interaction, page_number: int = 0):
        self.update_buttons()
        page = self.pages[page_number]
        await interaction.response.edit_message(embed=page, view=self)

    async def interaction_check(self, interaction: discord.Interaction):
        return self.user == interaction.user

    def update_buttons(self):
        self.clear_items()
        self.buttons["page_number"][
            "object"
        ].label = f"{self.current_page + 1}/{self.page_count + 1}"
        for key, button in self.buttons.items():
            if key != "page_number":
                if key == "<" or key == "<<":
                    if self.current_page <= 0:
                        button["object"].disabled = True
                    elif self.current_page >= 0:
                        button["object"].disabled = False
                elif key == ">" or key == ">>":
                    if self.current_page == self.page_count:
                        button["object"].disabled = True
                    elif self.current_page < self.page_count:
                        button["object"].disabled = False
            self.add_item(button["object"])

    async def send(self, msg):
        page = self.pages[0]
        await msg.edit(content=None, embed=page, view=self)


def create_pages(embeds, list, author, name):
    embed_pages = []
    for index, obj in enumerate(list):
        embeds[index].description += f"{obj.username}"
        embeds[index].add_field(
            name=f"{name} {index + 1}", value=f"{list[index]}", inline=False
        )
        embeds[index].set_footer(
            icon_url=author.display_avatar, text=f"Requested by {author.name}"
        )
        embed_pages.append(embeds[index])
    return embed_pages
