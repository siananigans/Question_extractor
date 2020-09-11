import time, random, requests
import json
import asyncio
from aiohttp import ClientSession


async def random_requests(text, session, t):
    l = len(text.split('.'))
    num = l - 2

    j = {
        'text': text,
        'num': num
    }

    await asyncio.sleep(random.uniform(0.0, 1.0))

    if t % 2 != 0:
        start_time = time.time()
        response = await session.post(
            'http://questionextractor-env.eba-mqvb3tex.eu-west-1.elasticbeanstalk.com/extract/', data=j)
        current_time = time.time()

    else:
        start_time = time.time()
        response = await session.post('http://questionextractor-env-1.eu-west-1.elasticbeanstalk.com/', data=j)
        current_time = time.time()

    time_taken = current_time - start_time

    print("Request " + str(t + 1) + " took: " + str(time_taken) + " seconds to complete with status: " + str(response.status))

    return time_taken


async def main():
    test_texts = ['The Kyrgyz Republic is seen by many experts as backsliding from the high point it reached in the mid-1990s with a \
    hastily pushed through referendum in 2003, reducing the legislative branch to one chamber with 75 deputies. The use of ink is only \
    one part of a general effort to show commitment towards more open elections - the German Embassy, the Soros Foundation and the Kyrgyz \
    government have all contributed to purchase transparent ballot boxes. The actual technology behind the ink is not that complicated. \
    The ink is sprayed on a persons left thumb. It dries and is not visible under normal light. However, the presence of ultraviolet light \
    (of the kind used to verify money) causes the ink to glow with a neon yellow light. At the entrance to each polling station, one election \
    official will scan voters fingers with UV lamp before allowing them to enter, and every voter will have his/her left thumb sprayed with ink \
    before receiving the ballot. If the ink shows under the UV light the voter will not be allowed to enter the polling station. Likewise, any \
    voter who refuses to be inked will not receive the ballot. These elections are assuming even greater significance because of two large factors \
    - the upcoming parliamentary elections are a prelude to a potentially regime changing presidential election in the Autumn as well as the echo of \
    recent elections in other former Soviet Republics, notably Ukraine and Georgia. The use of ink has been controversial - especially among groups \
    perceived to be pro-government.', 'In Serbia, for example, both Christian and Islamic leaders assured their populations that its use was not \
    contrary to religion.', 'More than half (55%) of the respondents said they were either concerned or very concerned that RFID tags would allow \
    businesses to track consumers via product purchases. Fifty nine percent of people said they were worried that RFID tags would allow data to be \
    used more freely by third parties. Ard Jan Vetham, Capgeminis principal consultant on RFID, said the survey showed that retailers needed to \
    inform and educate people about RFID before it would become accepted technology. Acceptance of new technologies always has a tipping point \
    at which consumers believe that benefits outweigh concerns. With the right RFID approach and ongoing communication with consumers, the industry \
    can reach this point. He said that the survey also showed people would accept RFID if they felt that the technology could mean a reduction in car \
    theft or faster recovery of stolen items. The tags are currently being used at one Tesco distribution centre in the UK - the tags allow the rapid \
    inventory of bulk items. They are also in use as a passcard for the M6 Toll in the Midlands, in the UK. Mr Vetham said the majority of \
    people surveyed (52%) believed that RFID tags could be read from a distance. He said that was a misconception based on a lack of awareness \
    of the technology. At least once consumer group - Consumers Against Supermarket Privacy Invasion and Numbering (Caspian) - has claimed that \
    RFID chips could be used to secretly identify people and the things they are carrying or wearing. All kinds of personal belongings, including \
    clothes, could constantly broadcast messages about their whereabouts and their owners, it warned. These awards reflect the enormous \
    achievements, progress and diversity that we have seen in that time. Halo 2 won the best Xbox game category, while Prince of Persia: \
    Warrior Within was adjudged the best GameCube title. The sports award went to Konamis Pro Evolution Soccer 4. Bafta said the significant \
    feature of this years awards was the number of non-traditional games. The originality award was won by PlayStation 2 title Singstar while \
    the childrens award went to GameCube bongo rhythm game Donkey Konga. The Handheld Award went to Colin McRae Rally 2005 while the mobile \
    category was won by Blue Tooth Byplanes. The audio award was won by Call of Duty: Finest Hour and Hitman: Contracts won the music award. \
    The laser bridges can route data at speeds up to 1.25gbps (2,000 times faster than a 512kbps broadband connection) but Tata is running its \
    hardware at more modest speeds of 1-2mbps. The lasers are also ideal for India because of its climate. Its particularly suitable as \
    the rain rate is a little low and its hardly ever foggy, he said. In places where rain is heavy and fog is common laser links can \
    struggle to maintain good connection speeds. The laser links also take far less time to set up and get working, said Mr Sridharan. \
    Once we get the other permissions, normal time period for set up is a few hours, he said. By contrast, he said, digging up roads \
    and laying cables can take weeks or months. This speed of set up has helped Tata with its aggressive expansion plans. Just over 12 \
    months ago the firm had customers in only about 70 towns and cities. But by the end of March the firm hopes to reach more than 1,000. \
    Speed is very important because of the pace of competition, said Mr Sridharan.', 'But the suit claims the chips also shut down the \
    cartridges at a predetermined date regardless of whether they are empty. The smart chip is dually engineered to prematurely register \
    ink depletion and to render a cartridge unusable through the use of a built-in expiration date that is not revealed to the consumer, \
    the suit said. The lawsuit is asking for restitution, damages and other compensation. The cost of printer cartridges has been a \
    contentious issue in Europe for the last 18 months. The price of inkjet printers has come down to as little as £34 but it could \
    cost up to £1,700 in running costs over an 18-month period due to cartridge, a study by Computeractive Magazine revealed last year. \
    The inkjet printer market has been the subject of an investigation by the UKs Office of Fair Trading (OFT), which concluded in a 2002 \
    report that retailers and manufacturers needed to make pricing more transparent for consumers.', 'It also capitalised on the growing \
    popularity of LAN gaming in the PC world - for the first time it became easy to link multiple game consoles together, allowing up to \
    16 players to battle against each other at the same time.', 'The game also inspired thousands of people to write their own fiction \
    based on the storyline and produce downloadable video clips of the many weird and wonderful things that can be done in the game. \
    It blew me away the first time someone managed to climb to the top of Halo, said Errera, referring to a fan who had created a \
    video of Master Chief scaling the landscape of the graphical world. Video clips of the more outrageous stunts that are possible thanks \
    to the games amazing physics engine are incredibly popular and some have attained a cult following. Speculation about the sequel \
    has seen every titbit analysed and poured over with all the intent of a forensic scientist examining a body. When early screenshots \
    of the game were released some people wrote essay-length articles highlighting everything from the texture of graphics to clues about \
    the story line. Errera said expectations of the sequel among fans were sky high. It does not feel like a game release any more. Somebody \
    told me this was the biggest single release of any product in Microsofts history. We are all just hoping that Bungie has got it right again.']

    futures = []
    i = 0
    t = 0
    async with ClientSession() as session:
        while i < 80:
            futures.append(loop.create_task(random_requests(test_texts[t], session, t)))
            i += 1
            if t == 4:
                t = 0
            else:
                t += 1

        response = await asyncio.gather(*futures)

        average = sum(response) / len(response)
        print("Average time for request: " + str(average))

        await session.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
