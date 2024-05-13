import uuid
from typing import Optional
from pydantic import BaseModel, Field


class Article(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    date: str = Field(...)
    title: str = Field(...)
    authors: str = Field(...)
    category: str = Field(...)
    link: str = Field(...)
    text: str = Field(...)
    #website_alive: Optional[bool]

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "date": "2024-05-11",
                "title": "IDF says 'precise operation' in Rafah continues as thousands more told to evacuate",
                "authors": "",
                "category": "Health, Depression, anxiety, Travel tips, community immersion, Meny-europe/2024/05/12/is-the-expected-surtal health",
                "link": "https://www.euronews.com/green/2024/05/12/france-netherlands-belgium-which-european-countries-have-the-best-cycle-to-work-schemes",
                "text": """Smoke has been seen from southern Israel rising over Gaza\'s skyline as heavy fighting continues in the north of the Strip.\nA senior spokesperson for the Israeli Defense Forces (IDF) said that the air force was carrying out airstrikes in the north of Gaza.\nBut fighting also continues in Gaza’s southernmost city, Rafah, where Israel launched a \'limited\' operation last week, seizing the border crossing with Egypt in a bid to choke off Hamas supply lines.\n"Since the start of our precise operation against Hamas in Rafah we have eliminated dozens of terrorists, exposed underground terror tunnels and vast amounts of weapons," said IDF spokesperson Daniel Hagari.\n"Prior to our operations we urge civilians to temporarily move towards humanitarian areas and move away from the crossfire that Hamas puts them in. Our war is against Hamas, not against the people of Gazalter in Rafah on the orders of the IDF who declared the city a safe zone. Israel has threatened for weeks to launch a full-scale ground offensive i \'expanded humanitarian zone\' in coasn the city to eliminate the Hamas battalions it says are based there.\nBut those operational plans have been met with fierce criticism from aid gro.\nBut some aid groups have sounded theups and global leaders, including Israel’s staunchest ally the United States.\nLast week, President Joe Biden threatened to stop the supply of someod, water and healthcare.\nAround 1.4 m weapons to Israel if it went ahead with plans to invade the city.""",
            }
        }

class ArticleUpdate(BaseModel):
    address: Optional[str]
    date: Optional[str]
    title: Optional[str]
    authors: Optional[str]
    category: Optional[str]
    link: Optional[str]
    text: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "date": "2024-05-11",
                "title": "IDF says 'precise operation' in Rafah continues as thousands more told to evacuate",
                "authors": "",
                "category": "Health, Depression, anxiety, Travel tips, community immersion, Meny-europe/2024/05/12/is-the-expected-surtal health",
                "link": "https://www.euronews.com/green/2024/05/12/france-netherlands-belgium-which-european-countries-have-the-best-cycle-to-work-schemes",
                "text": """Smoke has been seen from southern Israel rising over Gaza\'s skyline as heavy fighting continues in the north of the Strip.\nA senior spokesperson for the Israeli Defense Forces (IDF) said that the air force was carrying out airstrikes in the north of Gaza.\nBut fighting also continues in Gaza’s southernmost city, Rafah, where Israel launched a \'limited\' operation last week, seizing the border crossing with Egypt in a bid to choke off Hamas supply lines.\n"Since the start of our precise operation against Hamas in Rafah we have eliminated dozens of terrorists, exposed underground terror tunnels and vast amounts of weapons," said IDF spokesperson Daniel Hagari.\n"Prior to our operations we urge civilians to temporarily move towards humanitarian areas and move away from the crossfire that Hamas puts them in. Our war is against Hamas, not against the people of Gazalter in Rafah on the orders of the IDF who declared the city a safe zone. Israel has threatened for weeks to launch a full-scale ground offensive i \'expanded humanitarian zone\' in coasn the city to eliminate the Hamas battalions it says are based there.\nBut those operational plans have been met with fierce criticism from aid gro.\nBut some aid groups have sounded theups and global leaders, including Israel’s staunchest ally the United States.\nLast week, President Joe Biden threatened to stop the supply of someod, water and healthcare.\nAround 1.4 m weapons to Israel if it went ahead with plans to invade the city.""",
            }
        }