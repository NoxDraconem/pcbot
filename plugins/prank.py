""" Prank plugin

This plugin returns an image, pranking a user.

For on_message(), args is a list of all arguments split with shlex.

Commands:
!prank
"""

import discord
import asyncio
from PIL import Image, ImageDraw, ImageFont

commands = {
    "prank": {
        "usage": "!prank [user]",
        "desc": "Prank your favourite user!\n"
                "`user` is optional and will specify the user. This is either a @mention, username (will detect users) "
                "or whatever you'd like."
    }
}

prank_path = "plugins/prank/"

image_base = Image.open(prank_path + "discord_prank.png").convert("RGBA")
image_font = ImageFont.truetype(prank_path + "American Captain.ttf", 50)
image_width, image_height = image_base.size


@asyncio.coroutine
def on_message(client: discord.Client, message: discord.Message, args: list):
    if args[0] == "!prank":
        name = "IT'S A"

        # Set the name to a discord user if found
        if len(args) > 1:
            name = " ".join(args[1:])
            member = client.find_member(message.server, name)

            if member:
                name = member.name

        name = name.upper()

        # Initialize the image
        image_text = Image.new("RGBA", image_base.size, (255, 255, 255, 0))
        image_context = ImageDraw.Draw(image_text)

        # Set x and y coordinates for centered text
        width, height = image_context.textsize(name, image_font)
        x = (image_width-width) / 2
        y = (height / 2 - 5)

        # Draw border
        image_context.text((x-2, y), name, font=image_font, fill=(0, 0, 0, 255))
        image_context.text((x+2, y), name, font=image_font, fill=(0, 0, 0, 255))
        image_context.text((x, y-2), name, font=image_font, fill=(0, 0, 0, 255))
        image_context.text((x, y+2), name, font=image_font, fill=(0, 0, 0, 255))

        # Draw text
        image_context.text((x, y), name, font=image_font, fill=(255, 255, 255, 255))

        # Combine the base image with the font image
        image = Image.alpha_composite(image_base, image_text)

        # Save and send the image
        image.save(prank_path + "pranked.png")
        yield from client.send_file(message.channel, prank_path + "pranked.png")