from sprites import Troll, Fruits, IceBlocks, Player, iceblocks, trolls, fruits, players
from settings import SCREEN_HEIGHT, SCREEN_WIDTH
lv1_round1 = [
        [Troll(130,224,iceblocks,trolls),
        Troll(730,224,iceblocks,trolls)],

        [Fruits(110,y,"grapes",fruits,iceblocks) for y in range(144,550,58)] + 
        [Fruits(5*40 + 20 + 50,3*58 + 29 + 50,"grapes",fruits,iceblocks),Fruits(5*40 + 20 + 50,5*58 + 29 + 50,"grapes",fruits,iceblocks), Fruits(12*40 + 20 + 50,3*58 + 29 + 50,"grapes",fruits,iceblocks),Fruits(12*40 + 20 + 50,5*58 + 29 + 50,"grapes",fruits,iceblocks)] +
        [Fruits(110+15*40,y,"grapes",fruits,iceblocks) for y in range(144,550,58)],

        [IceBlocks(50,y) for y in range(50,622-58,58)] + [IceBlocks(730,y) for y in range(50,622-58,58)] + 
        [IceBlocks(x,50) for x in range(50+40,820-50-40,40)] + [IceBlocks(x,622-50-58) for x in range(50+40,820-50-40,40)] + 
        [IceBlocks(50+4*40,y) for y in range(50+58*2,50+58*7,58)] + [IceBlocks(50+13*40,y) for y in range(50+58*2,50+58*7,58)] + 
        [IceBlocks(50+5*40,50+58*2),IceBlocks(50+12*40,50+58*2),IceBlocks(50+5*40,50+58*6),IceBlocks(50+12*40,50+58*6)],

        [Player(450,SCREEN_HEIGHT-50 -58*2,iceblocks,trolls,fruits)],
        ]

lv1_round2 = [
        [troll for troll in trolls],

        [Fruits(110,y,"peach",fruits,iceblocks) for y in range(144,144+58*2,58)] + 
        [Fruits(110,y,"peach",fruits,iceblocks) for y in range(550-58,550-58*3,-58)] + 
        [Fruits(110+15*40,y,"peach",fruits,iceblocks) for y in range(144,144+58*2,58)] + 
        [Fruits(110+15*40,y,"peach",fruits,iceblocks) for y in range(550-58,550-58*3,-58)] + 
        [Fruits(110+40,144,"peach",fruits,iceblocks),Fruits(110+40,550-58,"peach",fruits,iceblocks),Fruits(110+14*40,144,"peach",fruits,iceblocks),Fruits(110+14*40,550-58,"peach",fruits,iceblocks)] +
        [Fruits(5*40 + 20 + 50,3*58 + 29 + 50,"peach",fruits,iceblocks),Fruits(5*40 + 20 + 50,5*58 + 29 + 50,"peach",fruits,iceblocks), Fruits(12*40 + 20 + 50,3*58 + 29 + 50,"peach",fruits,iceblocks),Fruits(12*40 + 20 + 50,5*58 + 29 + 50,"peach",fruits,iceblocks)],

        [iceblock for iceblock in iceblocks],

        [player for player in players],
        ]

lv1_round3 = [
        [troll for troll in trolls],

        [Fruits(x,144,"pear",fruits,iceblocks) for x in range(110,820-50-40,40)] + 
        [Fruits(x,550-58,"pear",fruits,iceblocks) for x in range(110,820-50-40,40)] + 
        [Fruits(110,y,"pear",fruits,iceblocks) for y in range(144+58,550-58,58)] +
        [Fruits(110+15*40,y,"pear",fruits,iceblocks) for y in range(144+58,550-58,58)] +
        [Fruits(4*40 + 20 + 50,y,"pear",fruits,iceblocks) for y in range(2*58 + 29 + 50,7*58 + 29 + 50,58)] +
        [Fruits(13*40 + 20 + 50,y,"pear",fruits,iceblocks) for y in range(2*58 + 29 + 50,7*58 + 29 + 50,58)] +
        [Fruits(5*40 + 20 + 50,2*58 + 29 + 50,"pear",fruits,iceblocks),Fruits(5*40 + 20 + 50,6*58 + 29 + 50,"pear",fruits,iceblocks), Fruits(12*40 + 20 + 50,2*58 + 29 + 50,"pear",fruits,iceblocks),Fruits(12*40 + 20 + 50,6*58 + 29 + 50,"pear",fruits,iceblocks)],

        [iceblock for iceblock in iceblocks],

        [player for player in players],
        ]

lv2_round1 = [
        [Troll(250,224,iceblocks,trolls),
        Troll(610,224,iceblocks,trolls),
        Troll(130,282,iceblocks,trolls),
        Troll(450,SCREEN_HEIGHT-50 -58*2,iceblocks,trolls),
        Troll(730,398,iceblocks,trolls)],

        [Fruits(110,y,"strawberry",fruits,iceblocks) for y in range(144,550,58)] + 
        [Fruits(4*40 + 20 + 50,1*58 + 29 + 50,"strawberry",fruits,iceblocks),Fruits(4*40 + 20 + 50,5*58 + 29 + 50,"strawberry",fruits,iceblocks),Fruits(5*40 + 20 + 50,7*58 + 29 + 50,"strawberry",fruits,iceblocks),Fruits(9*40 + 20 + 50,7*58 + 29 + 50,"strawberry",fruits,iceblocks),Fruits(6*40 + 20 + 50,5*58 + 29 + 50,"strawberry",fruits,iceblocks), Fruits(13*40 + 20 + 50,58 + 29 + 50,"strawberry",fruits,iceblocks),Fruits(13*40 + 20 + 50,4*58 + 29 + 50,"strawberry",fruits,iceblocks)] +
        [Fruits(110+15*40,y,"strawberry",fruits,iceblocks) for y in range(282+29,492,58)],

        [IceBlocks(50,y) for y in range(50,622-58,58)] + [IceBlocks(730,y) for y in range(50,622-58,58)] + 
        [IceBlocks(x,50) for x in range(50+40,820-50-40,40)] + [IceBlocks(x,622-50-58) for x in range(50+40,820-50-40,40)] + 
        [IceBlocks(50+4*40,y) for y in range(50+58*6,50+58*8,58)] + [IceBlocks(50+11*40,y) for y in range(50+58*1,50+58*8,58)] +
        [IceBlocks(50+5*40,y) for y in range(50+58*1,50+58*7,58)] + [IceBlocks(50+13*40,y) for y in range(50+58*5,50+58*8,58)] +
        [IceBlocks(50+3*40,y) for y in range(50+58*1,50+58*8,58)] + [IceBlocks(50+14*40,y) for y in range(50+58*1,50+58*8,58)] +
        [IceBlocks(50+2*40,y) for y in range(50+58*1,50+58*8,58)] + [IceBlocks(50+12*40,y) for y in range(50+58*1,50+58*8,58)] +
        [IceBlocks(50+6*40,y) for y in range(50+58*1,50+58*5,58)] + [IceBlocks(x,SCREEN_HEIGHT-50 -58*3) for x in range(50+40*6,50+40*11,40)] +
        [IceBlocks(50+10*40,50+58*7)] +
        [IceBlocks(x,50+2*58) for x in range(50+40*7,50+40*11,40)] + [IceBlocks(50+15*40,y) for y in range(50+58*1,50+58*8,58)] +
        [IceBlocks(50+16*40,y) for y in range(50+58*1,50+58*4,58)],

        [Player(370,50 + 58,iceblocks,trolls,fruits)],
        ]

lv2_round2 = [
        [troll for troll in trolls],

        [Fruits(50 + col * 40 +20, 50 + row * 58 + 29, "orange", fruits, iceblocks)
        for col in range(0,18) for row in range(0,4,2)] +
        [Fruits(50 + col * 40 +20, 622 - 50 - row * 58 - 29, "orange", fruits, iceblocks)
        for col in range(0,18) for row in range(0,4,2)] +

        [Fruits(50 + col * 40 +20, 224 + row * 58 + 29, "orange", fruits, iceblocks)
        for col in range(0,7) for row in range(0,4,2)] +
        [Fruits(50 + col * 40 +20, 224 + row * 58 + 29, "orange", fruits, iceblocks)
        for col in range(11,18) for row in range(0,4,2)],
        

        [Iceblock for Iceblock in iceblocks],

        [player for player in players],
        ]

lv2_round3 = [
        [troll for troll in trolls],

        [Fruits(50 + x * 40 + 20, 50 + 2 * 58 + 29,"pepper",fruits,iceblocks) for x in range(7, 11)] +
        [Fruits(50 + x * 40 + 20, 50 + 6 * 58 + 29,"pepper",fruits,iceblocks) for x in range(7, 11)] +
        [Fruits(50 + 6 * 40 + 20, 50 + 3 * 58 + 29,"pepper",fruits,iceblocks),
        Fruits(50 + 6 * 40 + 20, 50 + 4 * 58 + 29,"pepper",fruits,iceblocks),
        Fruits(50 + 6 * 40 + 20, 50 + 5 * 58 + 29,"pepper",fruits,iceblocks),
        Fruits(50 + 11 * 40 + 20, 50 + 3 * 58 + 29,"pepper",fruits,iceblocks),
        Fruits(50 + 11 * 40 + 20, 50 + 4 * 58 + 29,"pepper",fruits,iceblocks),
        Fruits(50 + 11 * 40 + 20, 50 + 5 * 58 + 29,"pepper",fruits,iceblocks)],

        [Iceblock for Iceblock in iceblocks],

        [player for player in players],
        ]

lv3_round1 = [
        [Troll(330,50+58,iceblocks,trolls),
        Troll(410,50+58,iceblocks,trolls),
        Troll(530,50+58,iceblocks,trolls),
        Troll(410,50+58*7,iceblocks,trolls),
        Troll(530,50+58*7,iceblocks,trolls),
        Troll(330,50+58*7,iceblocks,trolls)],

        [Fruits(70,y,"lemon",fruits,iceblocks) for y in range(144,550,58*2)] + 
        [Fruits(70 + 40*1,y,"lemon",fruits,iceblocks) for y in range(144-58,550+58,58*2)] + 
        [Fruits(70 + 40*2,y,"lemon",fruits,iceblocks) for y in range(144,550,58*2)] + 
        [Fruits(70 + 40*3,y,"lemon",fruits,iceblocks) for y in range(144-58,550+58,58*2)] + 
        [Fruits(70 + 40*4,y,"lemon",fruits,iceblocks) for y in range(144,550,58*2)] + 
        [Fruits(70 + 40*5,y,"lemon",fruits,iceblocks) for y in range(144-58,550+58,58*2)] + 
        [Fruits(70 + 40*6,y,"lemon",fruits,iceblocks) for y in range(144,550,58*2)] +
        [Fruits(70 + 40*11,y,"lemon",fruits,iceblocks) for y in range(144,550,58*2)] + 
        [Fruits(70 + 40*12,y,"lemon",fruits,iceblocks) for y in range(144-58,550+58,58*2)] + 
        [Fruits(70 + 40*13,y,"lemon",fruits,iceblocks) for y in range(144,550,58*2)] + 
        [Fruits(70 + 40*14,y,"lemon",fruits,iceblocks) for y in range(144-58,550+58,58*2)] + 
        [Fruits(70 + 40*15,y,"lemon",fruits,iceblocks) for y in range(144,550,58*2)] + 
        [Fruits(70 + 40*16,y,"lemon",fruits,iceblocks) for y in range(144-58,550+58,58*2)] + 
        [Fruits(70 + 40*17,y,"lemon",fruits,iceblocks) for y in range(144,550,58*2)],

        [IceBlocks(50,y) for y in range(50,622-58,58*2)] + [IceBlocks(90,y) for y in range(50+58,622-58*2,58*2)] + 
        [IceBlocks(130,y) for y in range(50,622-58,58*2)] + [IceBlocks(170,y) for y in range(50+58,622-58*2,58*2)] + 
        [IceBlocks(210,y) for y in range(50,622-58,58*2)] + [IceBlocks(250,y) for y in range(50+58,622-58*2,58*2)] + 
        [IceBlocks(290,y) for y in range(50,622-58,58*2)] + [IceBlocks(290+5*40,y) for y in range(50,622-58,58*2)] + 
        [IceBlocks(290+6*40,y) for y in range(50+58,622-58*2,58*2)] + [IceBlocks(290+7*40,y) for y in range(50,622-58,58*2)] + 
        [IceBlocks(290+8*40,y) for y in range(50+58,622-58*2,58*2)] + [IceBlocks(290+9*40,y) for y in range(50,622-58,58*2)] + 
        [IceBlocks(290+10*40,y) for y in range(50+58,622-58*2,58*2)] + [IceBlocks(290+11*40,y) for y in range(50,622-58,58*2)] +
        [IceBlocks(x,50) for x in range(330,290+5*40,40)] + [IceBlocks(330,50+58),IceBlocks(450,50+58)] + [IceBlocks(x,50+58*2) for x in range(330,290+5*40,40)] +
        [IceBlocks(x,50+58*6) for x in range(330,290+5*40,40)] + [IceBlocks(330,50+58*7),IceBlocks(450,50+58*7)] + [IceBlocks(x,50+58*8) for x in range(330,290+5*40,40)],

        [Player(730,SCREEN_HEIGHT-50 -58*2,iceblocks,trolls,fruits)],
        ]

lv3_round2 = [
        [troll for troll in trolls],

        [Fruits(50 + x * 40 + 20, 50 + 2 * 58 + 29,"kiwi",fruits,iceblocks) for x in range(7, 11)] +
        [Fruits(50 + x * 40 + 20, 50 + 6 * 58 + 29,"kiwi",fruits,iceblocks) for x in range(7, 11)] +
        [Fruits(50 + 6 * 40 + 20, 50 + 3 * 58 + 29,"kiwi",fruits,iceblocks),
        Fruits(50 + 6 * 40 + 20, 50 + 4 * 58 + 29,"kiwi",fruits,iceblocks),
        Fruits(50 + 6 * 40 + 20, 50 + 5 * 58 + 29,"kiwi",fruits,iceblocks),
        Fruits(50 + 11 * 40 + 20, 50 + 3 * 58 + 29,"kiwi",fruits,iceblocks),
        Fruits(50 + 11 * 40 + 20, 50 + 4 * 58 + 29,"kiwi",fruits,iceblocks),
        Fruits(50 + 11 * 40 + 20, 50 + 5 * 58 + 29,"kiwi",fruits,iceblocks)] +
        [Fruits(50 + x * 40 + 20, 50 + 1 * 58 + 29,"kiwi",fruits,iceblocks) for x in range(5, 13)] +
        [Fruits(50 + x * 40 + 20, 50 + 7 * 58 + 29,"kiwi",fruits,iceblocks) for x in range(5, 13)] +
        [Fruits(50 + 5 * 40 + 20, 50 + y * 58 + 29,"kiwi",fruits,iceblocks) for y in range(2,6)] +
        [Fruits(50 + 12 * 40 + 20, 50 + y * 58 + 29,"kiwi",fruits,iceblocks) for y in range(2,6)] +
        [Fruits(50 + x * 40 + 20, 50 + 29,"kiwi",fruits,iceblocks) for x in range(3, 15)] +
        [Fruits(50 + x * 40 + 20, 50 + 8 * 58 + 29,"kiwi",fruits,iceblocks) for x in range(3, 15)] +
        [Fruits(50 + 2 * 40 + 20, 50 + y * 58 + 29,"kiwi",fruits,iceblocks) for y in range(2,8)] +
        [Fruits(50 + 15 * 40 + 20, 50 + y * 58 + 29,"kiwi",fruits,iceblocks) for y in range(2,8)],
        
        [Iceblock for Iceblock in iceblocks],

        [player for player in players],
        ]

lv3_round3 = [
        [troll for troll in trolls],

        [Fruits(50 + x * 40 + 20, 50 + 2 * 58 + 29,"green apple",fruits,iceblocks) for x in range(7, 11)] +
        [Fruits(50 + x * 40 + 20, 50 + 6 * 58 + 29,"green apple",fruits,iceblocks) for x in range(7, 11)] +
        [Fruits(50 + 6 * 40 + 20, 50 + 3 * 58 + 29,"green apple",fruits,iceblocks),
        Fruits(50 + 6 * 40 + 20, 50 + 4 * 58 + 29,"green apple",fruits,iceblocks),
        Fruits(50 + 6 * 40 + 20, 50 + 5 * 58 + 29,"green apple",fruits,iceblocks),
        Fruits(50 + 11 * 40 + 20, 50 + 3 * 58 + 29,"green apple",fruits,iceblocks),
        Fruits(50 + 11 * 40 + 20, 50 + 4 * 58 + 29,"green apple",fruits,iceblocks),
        Fruits(50 + 11 * 40 + 20, 50 + 5 * 58 + 29,"green apple",fruits,iceblocks)] +
        [Fruits(50 + x * 40 + 20, 50 + 1 * 58 + 29,"green apple",fruits,iceblocks) for x in range(5, 13)] +
        [Fruits(50 + x * 40 + 20, 50 + 7 * 58 + 29,"green apple",fruits,iceblocks) for x in range(5, 13)] +
        [Fruits(50 + 5 * 40 + 20, 50 + y * 58 + 29,"green apple",fruits,iceblocks) for y in range(2,6)] +
        [Fruits(50 + 12 * 40 + 20, 50 + y * 58 + 29,"green apple",fruits,iceblocks) for y in range(2,6)] +
        [Fruits(50 + x * 40 + 20, 50 + 29,"green apple",fruits,iceblocks) for x in range(3, 15)] +
        [Fruits(50 + x * 40 + 20, 50 + 8 * 58 + 29,"green apple",fruits,iceblocks) for x in range(3, 15)] +
        [Fruits(50 + 2 * 40 + 20, 50 + y * 58 + 29,"green apple",fruits,iceblocks) for y in range(2,8)] +
        [Fruits(50 + 15 * 40 + 20, 50 + y * 58 + 29,"green apple",fruits,iceblocks) for y in range(2,8)],
        
        [Iceblock for Iceblock in iceblocks],

        [player for player in players],
        ]

# Simple way to get unaltered lists for any round of any level
def get_round(level, round):

    l1_r1 = [
            [Troll(130,224,iceblocks,trolls),
            Troll(730,224,iceblocks,trolls)],

            [Fruits(110,y,"grapes",fruits,iceblocks) for y in range(144,550,58)] + 
            [Fruits(5*40 + 20 + 50,3*58 + 29 + 50,"grapes",fruits,iceblocks),Fruits(5*40 + 20 + 50,5*58 + 29 + 50,"grapes",fruits,iceblocks), Fruits(12*40 + 20 + 50,3*58 + 29 + 50,"grapes",fruits,iceblocks),Fruits(12*40 + 20 + 50,5*58 + 29 + 50,"grapes",fruits,iceblocks)] +
            [Fruits(110+15*40,y,"grapes",fruits,iceblocks) for y in range(144,550,58)],
            [IceBlocks(50,y) for y in range(50,622-58,58)] + [IceBlocks(730,y) for y in range(50,622-58,58)] + 
            [IceBlocks(x,50) for x in range(50+40,820-50-40,40)] + [IceBlocks(x,622-50-58) for x in range(50+40,820-50-40,40)] + 
            [IceBlocks(50+4*40,y) for y in range(50+58*2,50+58*7,58)] + [IceBlocks(50+13*40,y) for y in range(50+58*2,50+58*7,58)] + 
            [IceBlocks(50+5*40,50+58*2),IceBlocks(50+12*40,50+58*2),IceBlocks(50+5*40,50+58*6),IceBlocks(50+12*40,50+58*6)],

            [Player(450,SCREEN_HEIGHT-50 -58*2,iceblocks,trolls,fruits)],
            ]

    l1_r2 = [
            [troll for troll in trolls],

            [Fruits(110,y,"peach",fruits,iceblocks) for y in range(144,144+58*2,58)] + 
            [Fruits(110,y,"peach",fruits,iceblocks) for y in range(550-58,550-58*3,-58)] + 
            [Fruits(110+15*40,y,"peach",fruits,iceblocks) for y in range(144,144+58*2,58)] + 
            [Fruits(110+15*40,y,"peach",fruits,iceblocks) for y in range(550-58,550-58*3,-58)] + 
            [Fruits(110+40,144,"peach",fruits,iceblocks),Fruits(110+40,550-58,"peach",fruits,iceblocks),Fruits(110+14*40,144,"peach",fruits,iceblocks),Fruits(110+14*40,550-58,"peach",fruits,iceblocks)] +
            [Fruits(5*40 + 20 + 50,3*58 + 29 + 50,"peach",fruits,iceblocks),Fruits(5*40 + 20 + 50,5*58 + 29 + 50,"peach",fruits,iceblocks), Fruits(12*40 + 20 + 50,3*58 + 29 + 50,"peach",fruits,iceblocks),Fruits(12*40 + 20 + 50,5*58 + 29 + 50,"peach",fruits,iceblocks)],

            [iceblock for iceblock in iceblocks],

            [player for player in players],
            ]

    l1_r3 = [
            [troll for troll in trolls],

            [Fruits(x,144,"pear",fruits,iceblocks) for x in range(110,820-50-40,40)] + 
            [Fruits(x,550-58,"pear",fruits,iceblocks) for x in range(110,820-50-40,40)] + 
            [Fruits(110,y,"pear",fruits,iceblocks) for y in range(144+58,550-58,58)] +
            [Fruits(110+15*40,y,"pear",fruits,iceblocks) for y in range(144+58,550-58,58)] +
            [Fruits(4*40 + 20 + 50,y,"pear",fruits,iceblocks) for y in range(2*58 + 29 + 50,7*58 + 29 + 50,58)] +
            [Fruits(13*40 + 20 + 50,y,"pear",fruits,iceblocks) for y in range(2*58 + 29 + 50,7*58 + 29 + 50,58)] +
            [Fruits(5*40 + 20 + 50,2*58 + 29 + 50,"pear",fruits,iceblocks),Fruits(5*40 + 20 + 50,6*58 + 29 + 50,"pear",fruits,iceblocks), Fruits(12*40 + 20 + 50,2*58 + 29 + 50,"pear",fruits,iceblocks),Fruits(12*40 + 20 + 50,6*58 + 29 + 50,"pear",fruits,iceblocks)],

            [iceblock for iceblock in iceblocks],

            [player for player in players],
            ]

    l2_r1 = [
            [Troll(250,224,iceblocks,trolls),
            Troll(610,224,iceblocks,trolls),
            Troll(130,282,iceblocks,trolls),
            Troll(450,SCREEN_HEIGHT-50 -58*2,iceblocks,trolls),
            Troll(730,398,iceblocks,trolls)],

            [Fruits(110,y,"strawberry",fruits,iceblocks) for y in range(144,550,58)] + 
            [Fruits(4*40 + 20 + 50,1*58 + 29 + 50,"strawberry",fruits,iceblocks),Fruits(4*40 + 20 + 50,5*58 + 29 + 50,"strawberry",fruits,iceblocks),Fruits(5*40 + 20 + 50,7*58 + 29 + 50,"strawberry",fruits,iceblocks),Fruits(9*40 + 20 + 50,7*58 + 29 + 50,"strawberry",fruits,iceblocks),Fruits(6*40 + 20 + 50,5*58 + 29 + 50,"strawberry",fruits,iceblocks), Fruits(13*40 + 20 + 50,58 + 29 + 50,"strawberry",fruits,iceblocks),Fruits(13*40 + 20 + 50,4*58 + 29 + 50,"strawberry",fruits,iceblocks)] +
            [Fruits(110+15*40,y,"strawberry",fruits,iceblocks) for y in range(282+29,492,58)],

            [IceBlocks(50,y) for y in range(50,622-58,58)] + [IceBlocks(730,y) for y in range(50,622-58,58)] + 
            [IceBlocks(x,50) for x in range(50+40,820-50-40,40)] + [IceBlocks(x,622-50-58) for x in range(50+40,820-50-40,40)] + 
            [IceBlocks(50+4*40,y) for y in range(50+58*6,50+58*8,58)] + [IceBlocks(50+11*40,y) for y in range(50+58*1,50+58*8,58)] +
            [IceBlocks(50+5*40,y) for y in range(50+58*1,50+58*7,58)] + [IceBlocks(50+13*40,y) for y in range(50+58*5,50+58*8,58)] +
            [IceBlocks(50+3*40,y) for y in range(50+58*1,50+58*8,58)] + [IceBlocks(50+14*40,y) for y in range(50+58*1,50+58*8,58)] +
            [IceBlocks(50+2*40,y) for y in range(50+58*1,50+58*8,58)] + [IceBlocks(50+12*40,y) for y in range(50+58*1,50+58*8,58)] +
            [IceBlocks(50+6*40,y) for y in range(50+58*1,50+58*5,58)] + [IceBlocks(x,SCREEN_HEIGHT-50 -58*3) for x in range(50+40*6,50+40*11,40)] +
            [IceBlocks(50+10*40,50+58*7)] +
            [IceBlocks(x,50+2*58) for x in range(50+40*7,50+40*11,40)] + [IceBlocks(50+15*40,y) for y in range(50+58*1,50+58*8,58)] +
            [IceBlocks(50+16*40,y) for y in range(50+58*1,50+58*4,58)],
            [Player(370,50 + 58,iceblocks,trolls,fruits)],
            ]

    l2_r2 = [
            [troll for troll in trolls],

            [Fruits(50 + col * 40 +20, 50 + row * 58 + 29, "orange", fruits, iceblocks)
            for col in range(0,18) for row in range(0,4,2)] +
            [Fruits(50 + col * 40 +20, 622 - 50 - row * 58 - 29, "orange", fruits, iceblocks)
            for col in range(0,18) for row in range(0,4,2)] +

            [Fruits(50 + col * 40 +20, 224 + row * 58 + 29, "orange", fruits, iceblocks)
            for col in range(0,7) for row in range(0,4,2)] +
            [Fruits(50 + col * 40 +20, 224 + row * 58 + 29, "orange", fruits, iceblocks)
            for col in range(11,18) for row in range(0,4,2)],
            

            [Iceblock for Iceblock in iceblocks],
            [player for player in players],
            ]

    l2_r3 = [
            [troll for troll in trolls],

            [Fruits(50 + x * 40 + 20, 50 + 2 * 58 + 29,"pepper",fruits,iceblocks) for x in range(7, 11)] +
            [Fruits(50 + x * 40 + 20, 50 + 6 * 58 + 29,"pepper",fruits,iceblocks) for x in range(7, 11)] +
            [Fruits(50 + 6 * 40 + 20, 50 + 3 * 58 + 29,"pepper",fruits,iceblocks),
            Fruits(50 + 6 * 40 + 20, 50 + 4 * 58 + 29,"pepper",fruits,iceblocks),
            Fruits(50 + 6 * 40 + 20, 50 + 5 * 58 + 29,"pepper",fruits,iceblocks),
            Fruits(50 + 11 * 40 + 20, 50 + 3 * 58 + 29,"pepper",fruits,iceblocks),
            Fruits(50 + 11 * 40 + 20, 50 + 4 * 58 + 29,"pepper",fruits,iceblocks),
            Fruits(50 + 11 * 40 + 20, 50 + 5 * 58 + 29,"pepper",fruits,iceblocks)],

            [Iceblock for Iceblock in iceblocks],
            [player for player in players],
            ]

    l3_r1 = [
        [Troll(330,50+58,iceblocks,trolls),
        Troll(410,50+58,iceblocks,trolls),
        Troll(530,50+58,iceblocks,trolls),
        Troll(410,50+58*7,iceblocks,trolls),
        Troll(530,50+58*7,iceblocks,trolls),
        Troll(330,50+58*7,iceblocks,trolls)],

        [Fruits(70,y,"lemon",fruits,iceblocks) for y in range(144,550,58*2)] + 
        [Fruits(70 + 40*1,y,"lemon",fruits,iceblocks) for y in range(144-58,550+58,58*2)] + 
        [Fruits(70 + 40*2,y,"lemon",fruits,iceblocks) for y in range(144,550,58*2)] + 
        [Fruits(70 + 40*3,y,"lemon",fruits,iceblocks) for y in range(144-58,550+58,58*2)] + 
        [Fruits(70 + 40*4,y,"lemon",fruits,iceblocks) for y in range(144,550,58*2)] + 
        [Fruits(70 + 40*5,y,"lemon",fruits,iceblocks) for y in range(144-58,550+58,58*2)] + 
        [Fruits(70 + 40*6,y,"lemon",fruits,iceblocks) for y in range(144,550,58*2)] +
        [Fruits(70 + 40*11,y,"lemon",fruits,iceblocks) for y in range(144,550,58*2)] + 
        [Fruits(70 + 40*12,y,"lemon",fruits,iceblocks) for y in range(144-58,550+58,58*2)] + 
        [Fruits(70 + 40*13,y,"lemon",fruits,iceblocks) for y in range(144,550,58*2)] + 
        [Fruits(70 + 40*14,y,"lemon",fruits,iceblocks) for y in range(144-58,550+58,58*2)] + 
        [Fruits(70 + 40*15,y,"lemon",fruits,iceblocks) for y in range(144,550,58*2)] + 
        [Fruits(70 + 40*16,y,"lemon",fruits,iceblocks) for y in range(144-58,550+58,58*2)] + 
        [Fruits(70 + 40*17,y,"lemon",fruits,iceblocks) for y in range(144,550,58*2)],

        [IceBlocks(50,y) for y in range(50,622-58,58*2)] + [IceBlocks(90,y) for y in range(50+58,622-58*2,58*2)] + 
        [IceBlocks(130,y) for y in range(50,622-58,58*2)] + [IceBlocks(170,y) for y in range(50+58,622-58*2,58*2)] + 
        [IceBlocks(210,y) for y in range(50,622-58,58*2)] + [IceBlocks(250,y) for y in range(50+58,622-58*2,58*2)] + 
        [IceBlocks(290,y) for y in range(50,622-58,58*2)] + [IceBlocks(290+5*40,y) for y in range(50,622-58,58*2)] + 
        [IceBlocks(290+6*40,y) for y in range(50+58,622-58*2,58*2)] + [IceBlocks(290+7*40,y) for y in range(50,622-58,58*2)] + 
        [IceBlocks(290+8*40,y) for y in range(50+58,622-58*2,58*2)] + [IceBlocks(290+9*40,y) for y in range(50,622-58,58*2)] + 
        [IceBlocks(290+10*40,y) for y in range(50+58,622-58*2,58*2)] + [IceBlocks(290+11*40,y) for y in range(50,622-58,58*2)] +
        [IceBlocks(x,50) for x in range(330,290+5*40,40)] + [IceBlocks(330,50+58),IceBlocks(450,50+58)] + [IceBlocks(x,50+58*2) for x in range(330,290+5*40,40)] +
        [IceBlocks(x,50+58*6) for x in range(330,290+5*40,40)] + [IceBlocks(330,50+58*7),IceBlocks(450,50+58*7)] + [IceBlocks(x,50+58*8) for x in range(330,290+5*40,40)],

        [Player(730,SCREEN_HEIGHT-50 -58*2,iceblocks,trolls,fruits)],
        ]

    l3_r2 = [
        [troll for troll in trolls],

        [Fruits(50 + x * 40 + 20, 50 + 2 * 58 + 29,"kiwi",fruits,iceblocks) for x in range(7, 11)] +
        [Fruits(50 + x * 40 + 20, 50 + 6 * 58 + 29,"kiwi",fruits,iceblocks) for x in range(7, 11)] +
        [Fruits(50 + 6 * 40 + 20, 50 + 3 * 58 + 29,"kiwi",fruits,iceblocks),
        Fruits(50 + 6 * 40 + 20, 50 + 4 * 58 + 29,"kiwi",fruits,iceblocks),
        Fruits(50 + 6 * 40 + 20, 50 + 5 * 58 + 29,"kiwi",fruits,iceblocks),
        Fruits(50 + 11 * 40 + 20, 50 + 3 * 58 + 29,"kiwi",fruits,iceblocks),
        Fruits(50 + 11 * 40 + 20, 50 + 4 * 58 + 29,"kiwi",fruits,iceblocks),
        Fruits(50 + 11 * 40 + 20, 50 + 5 * 58 + 29,"kiwi",fruits,iceblocks)] +

        [Fruits(50 + x * 40 + 20, 50 + 1 * 58 + 29,"kiwi",fruits,iceblocks) for x in range(5, 13)] +
        [Fruits(50 + x * 40 + 20, 50 + 7 * 58 + 29,"kiwi",fruits,iceblocks) for x in range(5, 13)] +
        [Fruits(50 + 5 * 40 + 20, 50 + y * 58 + 29,"kiwi",fruits,iceblocks) for y in range(2,6)] +
        [Fruits(50 + 12 * 40 + 20, 50 + y * 58 + 29,"kiwi",fruits,iceblocks) for y in range(2,6)] +
        
        [Fruits(50 + x * 40 + 20, 50 + 29,"kiwi",fruits,iceblocks) for x in range(3, 15)] +
        [Fruits(50 + x * 40 + 20, 50 + 8 * 58 + 29,"kiwi",fruits,iceblocks) for x in range(3, 15)] +
        [Fruits(50 + 2 * 40 + 20, 50 + y * 58 + 29,"kiwi",fruits,iceblocks) for y in range(2,8)] +
        [Fruits(50 + 15 * 40 + 20, 50 + y * 58 + 29,"kiwi",fruits,iceblocks) for y in range(2,8)],

        [Iceblock for Iceblock in iceblocks],

        [player for player in players],
        ]

    l3_r3 = [
        [troll for troll in trolls],

        [Fruits(50 + x * 40 + 20, 50 + 2 * 58 + 29,"green apple",fruits,iceblocks) for x in range(7, 11)] +
        [Fruits(50 + x * 40 + 20, 50 + 6 * 58 + 29,"green apple",fruits,iceblocks) for x in range(7, 11)] +
        [Fruits(50 + 6 * 40 + 20, 50 + 3 * 58 + 29,"green apple",fruits,iceblocks),
        Fruits(50 + 6 * 40 + 20, 50 + 4 * 58 + 29,"green apple",fruits,iceblocks),
        Fruits(50 + 6 * 40 + 20, 50 + 5 * 58 + 29,"green apple",fruits,iceblocks),
        Fruits(50 + 11 * 40 + 20, 50 + 3 * 58 + 29,"green apple",fruits,iceblocks),
        Fruits(50 + 11 * 40 + 20, 50 + 4 * 58 + 29,"green apple",fruits,iceblocks),
        Fruits(50 + 11 * 40 + 20, 50 + 5 * 58 + 29,"green apple",fruits,iceblocks)] +
        [Fruits(50 + x * 40 + 20, 50 + 1 * 58 + 29,"green apple",fruits,iceblocks) for x in range(5, 13)] +
        [Fruits(50 + x * 40 + 20, 50 + 7 * 58 + 29,"green apple",fruits,iceblocks) for x in range(5, 13)] +
        [Fruits(50 + 5 * 40 + 20, 50 + y * 58 + 29,"green apple",fruits,iceblocks) for y in range(2,6)] +
        [Fruits(50 + 12 * 40 + 20, 50 + y * 58 + 29,"green apple",fruits,iceblocks) for y in range(2,6)] +
        [Fruits(50 + x * 40 + 20, 50 + 29,"green apple",fruits,iceblocks) for x in range(3, 15)] +
        [Fruits(50 + x * 40 + 20, 50 + 8 * 58 + 29,"green apple",fruits,iceblocks) for x in range(3, 15)] +
        [Fruits(50 + 2 * 40 + 20, 50 + y * 58 + 29,"green apple",fruits,iceblocks) for y in range(2,8)] +
        [Fruits(50 + 15 * 40 + 20, 50 + y * 58 + 29,"green apple",fruits,iceblocks) for y in range(2,8)],
        
        [Iceblock for Iceblock in iceblocks],

        [player for player in players],
        ]
    
    if level == 1 == round:
        return l1_r1
    elif level == 1 and round == 2:
        return l1_r2
    elif level == 1 and round == 3:
        return l1_r3
    elif level == 2 and round == 1:
        return l2_r1
    elif level == 2 and round == 2:
        return l2_r2
    elif level == 2 and round == 3:
        return l2_r3
    elif level == 3 and round == 1:
        return l3_r1
    elif level == 3 and round == 2:
        return l3_r2
    elif level == 3 and round == 3:
        return l3_r3

# Dicionários para níveis
lv1_rounds = {1:lv1_round1, 2:lv1_round2, 3:lv1_round3}

lv2_rounds = {1: lv2_round1, 2: lv2_round2, 3: lv2_round3}

lv3_rounds = {1: lv3_round1, 2: lv3_round2, 3: lv3_round3}

lvs = [lv1_rounds,lv2_rounds,lv3_rounds]

round_final = 3
lv_final = 3
round_atual = 1
lv_atual = 1

counter = 0

