# This repository contains a game project in the Python programming language.
1
**The plot of the game:**

Game Start.
The player finds themselves shipwrecked on an island. His task is to find shelter and food, meet NPC players, and, by completing their quests, collect map elements that will allow the player to restore the ship and leave the island.
Game End.

**Island structure:**

The island consists of three parts. The first is the beach, made up of sand, rocks, and a few signposts. This is where the player begins the game and builds his ship. The second part is the village, where the player lives, eats, and interacts with NPC players. And the last, largest part is the forest. This is where the player will encounter enemies, try to obtain food, and complete quests.

**Characteristics of the characters**:

*Player:*

Health consists of two bars: the first is the food bar (initially 5) and the second is the air bar, needed if the player finds himself in water (initially 5). To survive, you need to fight forest animals, obtain their meat, and draw water from the well (колодец).

Equipment (opens in a separate tab) is initially empty. A sword is needed to fight enemies. To complete the game, you need to collect a hammer, a saw, and three map pieces (all of which can be obtained from NPC players). Food and water reserves are also shown here.

Abilities (functions): walking, eating (one food item is removed from the equipment, and the health bar increases (if it is not already full)), attacking, building (boat), drawing (забор, вычерпывание) water from the well, interacting with NPC players, reading the map (the map opens in a separate window).