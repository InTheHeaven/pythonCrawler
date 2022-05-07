import re
import aiofiles
import aiohttp
import asyncio
from lxml import etree
import os

class Section:
    def __init__(self, href, name, num):
        self.href = href
        self.name = name
        self.num = num

    async def download(self):
        source_code = await getCode(self.href)
        chapter_tree = etree.HTML(source_code)
        text = chapter_tree.xpath('//*[@id="BookText"]/text()')
        content = ""
        for it in text:
            content += it
        content = re.sub("\xa0", " ", content)
        # print(content)
        # print(self.name)
        # print(self.num)
        async with aiofiles.open(str(self.num) + "." + self.name + ".txt",
                                 "w", encoding="utf-8",
                                 errors="ignore") as writing:
            await writing.write(self.name + "\n" + content)

async def getCode(domain):
    async with aiohttp.ClientSession() as session:
        async with session.get(domain) as response:
            content = await response.text()
            return content

url_o = 'https://www.westnovel.com/hbtr/'


async def main():
    os.chdir("D:\It\CrawlerFlute\literature\霍比特人")
    code_o = await getCode(url_o)
    # print(code_o)
    o_tree = etree.HTML(code_o)
    href = o_tree.xpath("/html/body/div[4]/div/div/dl/dd/a/@href")
    name = o_tree.xpath("/html/body/div[4]/div/div/dl/dd/a/@title")
    # print(len(href), len(name))
    task = []
    for it in range(0, len(name)):
        chapter = Section('https://www.westnovel.com' + href[it],
                       name[it],
                       it + 1)
        task.append(asyncio.create_task(chapter.download()))
    await asyncio.wait(task)

if __name__ == "__main__":
    asyncio.run(main())
