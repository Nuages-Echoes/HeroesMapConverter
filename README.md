# HeroesMapConverter
Tool used to convert maps from different Heroes of Might and Magic. Objective first is to be able to convert maps to Olden Era, and then to other Horeos games.

To parse H3 files, I used the description found here 
https://github.com/HeroWO-js/h3m2json/blob/master/references/h3m_description.english.txt

I decided to not reuse the project directly as I intend to use python and not php.
Also, I am also using this project as test for vibe coding, so bug may abound.

How it works :
- project reads the files in /input directory
- files are converted to json format and stored in /outputjson directory
- file from /outputjson are read and converted to heroes file format

Why all the bother ?
Because by using the json format, I hope we will be able to convert heroes maps to any heroes using the common json file. In the long run it will save time to convert any file to json and then to whichever heroes format you want then to convert directly from heroesX to hereosY

Can I help ?
Yes you can, it's a pet project feel free to modify or clone it. Just don't sell it or make money out of it.

No UI ?
No, not yet. I'd like to make it work first and then think about UI. Also, I don't much about UI so it's harder for me to review or correct UI related bugs. Even if the project is vibe coded (because honestly setting up the parsing sucks) doesn't mean I don't look at it and modify it by hand.

Known Limitations
Converting maps with subterranean map to H2 ends in failure (no underground in H2)

Neutral heroes from H3 disappear in H2 maps (no neutral heroes in the game)
