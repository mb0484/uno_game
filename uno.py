import pygame
import pygame_widgets
import random

pygame.init()

display_width = 1000
display_height = 800

card_width = 83
card_height = 131
start_x_in_hand = 30

card_on_middle_x = (display_width / 2.0 - card_width / 2.0) - card_width / 2.0
card_on_middle_y = (display_height / 2.0 - card_height / 2.0)

deck_card_x = card_on_middle_x + card_width + 20
deck_card_y = card_on_middle_y

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
light_gray = (211,211,211)

pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 20)


#game settings
num_of_cards_to_draw_at_start = 6
num_of_card_repetitions_in_deck = 2
num_of_bot_players = 3
#easy, medium and hard -> for now it just affects game tempo
difficulty = 'easy'
FPS = 30



gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Club T.I.L.E.N corporations presents: UNO official')
clock = pygame.time.Clock()

dack_back_uno_card = pygame.image.load('card_images/uno_cover.png')

def are_cards_connected(card1, card2, player_turn):
    #check if plus 4 card
    if (card1.value == 13 and card1.color == None) or (card2.value == 13 and card2.color == None):
        return True
    #check if change color
    if (card1.value == 14 and card1.color == None) or (card2.value == 14 and card2.color == None):
        return True


    if card1.color == card2.color:
        return player_turn or card1.value == card2.value 
    return player_turn and card1.value == card2.value 

def pick_random_color():
    return random.choice(['blue', 'green', 'yellow', 'red'])

class Card(object):

    def __init__(self, c, v):
        self.color = c
        self.value = v
        self.update_image()

        self.position_x = 0.0
        self.position_y = 0.0

    def update_image(self):
        if (self.value <= 9):
            self.card_image = pygame.image.load('card_images/' + self.color + '_' + str(self.value) + '.png')
        #10 -> stop
        elif (self.value == 10):
            self.card_image = pygame.image.load('card_images/' + self.color + '_stop.png')
        #11 -> obrat
        elif (self.value == 11):
            self.card_image = pygame.image.load('card_images/' + self.color + '_obrat.png')
        #12 -> plus 2
        elif (self.value == 12):
            self.card_image = pygame.image.load('card_images/' + self.color + '_plus_2.png')
        #13 -> plus 4
        elif (self.value == 13):
            self.card_image = pygame.image.load('card_images/plus_4.png')
        #14 -> change color
        elif (self.value == 14):
            self.card_image = pygame.image.load('card_images/change_color.png')

    def update_position(self, x, y):
        self.position_x = x
        self.position_y = y

    def hover_over_card(self, x, y, card_in_the_middle, player_turn):
        if are_cards_connected(self, card_in_the_middle, player_turn):
            if x >= self.position_x and y >= self.position_y and  x <= (self.position_x + card_width) and y <= (self.position_y + card_height):
                return True

        return False


class player(object):

    def __init__(self, board):
        self.hand = list()
        self.board = board
        self.board.add_player(self)
        self.draw_cards(num_of_cards_to_draw_at_start)
        self.already_draw_this_turn = False
        self.chosen_color = None

    def add_card_in_hand(self, card):
        self.hand.append(card)
        self.update_card_positions()

    def update_card_positions(self):
        pos = 0
        pos_y = 1

        for card in self.hand:
            cur_x = start_x_in_hand + pos * (card_width + 5.0)
            cur_y = display_height - pos_y * (card_height + 10)

            if cur_x <= (display_width - card_width):
                card.update_position(cur_x, cur_y)
                pos += 1
            else:
                pos = 0
                pos_y += 1
                if pos_y == 3:
                    pos_y += 2
                cur_y = display_height - pos_y * (card_height + 10)
                cur_x = start_x_in_hand + pos * (card_width + 5.0)

                card.update_position(cur_x, cur_y)
                pos += 1


    def draw_cards(self, how_many):
        for _ in range(how_many):
            self.add_card_in_hand(self.board.deck.draw())



class Deck(object):

    def __init__(self):
        self.cards = list()

        for _ in range(num_of_card_repetitions_in_deck):
            #plus 4
            self.cards.append(Card(None, 13))
            self.cards.append(Card(None, 13))

            #change color
            self.cards.append(Card(None, 14))
            self.cards.append(Card(None, 14))

            self.cards.append(Card('blue', 0))
            self.cards.append(Card('blue', 1))
            self.cards.append(Card('blue', 2))
            self.cards.append(Card('blue', 3))
            self.cards.append(Card('blue', 4))
            self.cards.append(Card('blue', 5))
            self.cards.append(Card('blue', 6))
            self.cards.append(Card('blue', 7))
            self.cards.append(Card('blue', 8))
            self.cards.append(Card('blue', 9))
            self.cards.append(Card('blue', 10))
            self.cards.append(Card('blue', 11))
            self.cards.append(Card('blue', 12))

            self.cards.append(Card('yellow', 0))
            self.cards.append(Card('yellow', 1))
            self.cards.append(Card('yellow', 2))
            self.cards.append(Card('yellow', 3))
            self.cards.append(Card('yellow', 4))
            self.cards.append(Card('yellow', 5))
            self.cards.append(Card('yellow', 6))
            self.cards.append(Card('yellow', 7))
            self.cards.append(Card('yellow', 8))
            self.cards.append(Card('yellow', 9))
            self.cards.append(Card('yellow', 10))
            self.cards.append(Card('yellow', 11))
            self.cards.append(Card('yellow', 12))

            self.cards.append(Card('red', 0))
            self.cards.append(Card('red', 1))
            self.cards.append(Card('red', 2))
            self.cards.append(Card('red', 3))
            self.cards.append(Card('red', 4))
            self.cards.append(Card('red', 5))
            self.cards.append(Card('red', 6))
            self.cards.append(Card('red', 7))
            self.cards.append(Card('red', 8))
            self.cards.append(Card('red', 9))
            self.cards.append(Card('red', 10))
            self.cards.append(Card('red', 11))
            self.cards.append(Card('red', 12))

            self.cards.append(Card('green', 0))
            self.cards.append(Card('green', 1))
            self.cards.append(Card('green', 2))
            self.cards.append(Card('green', 3))
            self.cards.append(Card('green', 4))
            self.cards.append(Card('green', 5))
            self.cards.append(Card('green', 6))
            self.cards.append(Card('green', 7))
            self.cards.append(Card('green', 8))
            self.cards.append(Card('green', 9))
            self.cards.append(Card('green', 10))
            self.cards.append(Card('green', 11))
            self.cards.append(Card('green', 12))

        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop()
        
 
class board(object):

    def __init__(self):
        self.deck = Deck()
        self.cur_top_card = self.deck.draw()
        self.players = []
        self.cur_player = 1
        self.direction = 0

        self.stop_for_next_player = False
        self.next_player_must_draw = 0

        self.cur_bot_waiting_time = 0
        if difficulty == 'easy':
            self.expected_bot_waiting_time = FPS * 2.0
        elif difficulty == 'medium':
            self.expected_bot_waiting_time = FPS * 1.0
        elif difficulty == 'hard':
            self.expected_bot_waiting_time = FPS * 0.5

    def check_for_victory(self):
        for player_index, player in enumerate(self.players):
            if len(player.hand) == 0:
                print("Player " + str(player_index) + " wins!")
                return False
        return True

    def get_bot_players_info(self):
        bot_player_info = []

        for i in range(1, len(self.players)):
            bot_player_info.append(len(self.players[i].hand))

        return bot_player_info


    def put_card_on_top(self, card, color_if_change_color=None):
        #player put stop card on top
        if card.value == 10:
            self.stop_for_next_player = True
        #player put change direction card on top
        if card.value == 11:
            self.change_direction()
        #player put plus 2 card on top
        if card.value == 12:
            self.next_player_must_draw = 2
        #if plus 4 card
        if card.value == 13:
            self.next_player_must_draw = 4
            if color_if_change_color == None:
                card.color = pick_random_color()
            else:
                card.color = color_if_change_color
        #if change color card
        if card.value == 14:
            if color_if_change_color == None:
                card.color = pick_random_color()
            else:
                card.color = color_if_change_color

        self.cur_top_card = card

    def add_player(self, player):
        self.players.append(player)

    def change_direction(self):
        self.direction = (self.direction + 1) % 2

    def get_next_player_index(self):
        next_player_index = self.cur_player
        if self.direction == 0:
            next_player_index = (self.cur_player + 1) % len(self.players)
        elif self.direction == 1:
            next_player_index -= 1
            if next_player_index < 0:
                next_player_index = len(self.players) - 1

        return next_player_index

    def next_player(self):
        self.cur_player = self.get_next_player_index()

        if self.stop_for_next_player:
            self.cur_player = self.get_next_player_index()
            self.stop_for_next_player = False
        if self.next_player_must_draw:
            print("cur player must draw: ", self.next_player_must_draw)
            self.get_cur_player().draw_cards(self.next_player_must_draw)
            self.cur_player = self.get_next_player_index()
            self.next_player_must_draw = 0

    def get_cur_player(self):
        return self.players[self.cur_player]

    def bot_play_card_if_can(self, cur_bot_player, player_turn=True):
        for card in cur_bot_player.hand:
            if are_cards_connected(card, self.cur_top_card, player_turn):
                #here bot plays a card - for now, i just pick the first one
                self.put_card_on_top(card)
                cur_bot_player.hand.remove(card)
                return True
        return False

    def make_bot_move(self):
        if self.cur_bot_waiting_time >= self.expected_bot_waiting_time:
            self.cur_bot_waiting_time = 0

            cur_bot_player = self.players[self.cur_player]

            bot_played_a_card = self.bot_play_card_if_can(cur_bot_player)

            if not bot_played_a_card:
                cur_bot_player.draw_cards(1)
                #print("bot draws")

                self.bot_play_card_if_can(cur_bot_player)

            #bot finished it's move, so move to next player
            self.next_player()
        else:
            self.cur_bot_waiting_time += 1


def display_cards_in_hand(player):

    for card in player.hand:
        display_up_card(card.position_x, card.position_y, card)


def display_up_card(x, y, card):
    gameDisplay.blit(card.card_image, (x, y))

def draw_rect_around_image(image):
    pygame.draw.rect(image, red, (0, 0, image.get_rect().size[0] - 1, image.get_rect().size[1] - 1), 2)












main_board = board()
player_1 = player(main_board)

for _ in range(num_of_bot_players):
    player(main_board)

main_player_draw_a_card = False
cur_picked_color = None
put_card_on_top_after_color_choice = None

def reset_player_1_status():
    global main_player_draw_a_card, put_card_on_top_after_color_choice

    player_1.chosen_color = None
    put_card_on_top_after_color_choice = None
    main_player_draw_a_card = False

def skip_button_pressed(main_board):
    global main_player_draw_a_card

    if main_player_draw_a_card:
        reset_player_1_status()
        main_board.next_player()

def pick_color(player, color):
    player.chosen_color = color

#define all buttons
skip_button = pygame_widgets.Button(
        gameDisplay, display_width / 2.0 - 30, display_height / 2.0 - 120, 80, 30, text='Skip',
        fontSize=30, margin=10,
        inactiveColour=(255, 0, 0),
        pressedColour=(0, 255, 0), radius=20,
        onClick=lambda: skip_button_pressed(main_board)
    )

pick_color_red = pygame_widgets.Button(
        gameDisplay, display_width - 200, display_height / 2.0 - 140, 100, 50, text='Red',
        fontSize=30, margin=10,
        inactiveColour=(255, 0, 0),
        pressedColour=(0, 255, 0), radius=20,
        onClick=lambda: pick_color(player_1, 'red')
    )

pick_color_green = pygame_widgets.Button(
        gameDisplay, display_width - 200, display_height / 2.0 - 45, 100, 50, text='Green',
        fontSize=30, margin=10,
        inactiveColour=(0, 255, 0),
        pressedColour=(0, 255, 0), radius=20,
        onClick=lambda: pick_color(player_1, 'green')
    )

pick_color_blue = pygame_widgets.Button(
        gameDisplay, display_width - 200, display_height / 2.0 + 45, 100, 50, text='Blue',
        fontSize=30, margin=10,
        inactiveColour=(0, 0, 255),
        pressedColour=(0, 255, 0), radius=20,
        onClick=lambda: pick_color(player_1, 'blue')
    )

pick_color_yellow = pygame_widgets.Button(
        gameDisplay, display_width - 200, display_height / 2.0 + 140, 100, 50, text='Yellow',
        fontSize=30, margin=10,
        inactiveColour=(255, 255, 0),
        pressedColour=(0, 255, 0), radius=20,
        onClick=lambda: pick_color(player_1, 'yellow')
    )

    



game_running = True

while game_running:

    cur_player = main_board.get_cur_player()

    gameDisplay.fill(light_gray)
    display_cards_in_hand(player_1)

    #all events that happened
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            exit()

        cur_mouse_x, cur_mouse_y = pygame.mouse.get_pos()

        #markup cards if they can be played and player hovers over them
        for card in player_1.hand:
            if card.hover_over_card(cur_mouse_x, cur_mouse_y, main_board.cur_top_card, player_turn=cur_player == player_1):
                draw_rect_around_image(card.card_image)
            else:
                #update only if player is not chosing color
                if put_card_on_top_after_color_choice != card:
                    card.update_image()

        # if player_turn
        if cur_player == player_1 and not main_player_draw_a_card:
            if cur_mouse_x >= deck_card_x and cur_mouse_y >= deck_card_y and cur_mouse_x <= (deck_card_x + card_width) and cur_mouse_y <= (deck_card_y + card_height):
                draw_rect_around_image(dack_back_uno_card)
            else:
                dack_back_uno_card = pygame.image.load('card_images/uno_cover.png')

        #player clicked on card
        if event.type == pygame.MOUSEBUTTONDOWN:
            main_player_picked_something = False

            for card in player_1.hand:
                if card.hover_over_card(cur_mouse_x, cur_mouse_y, main_board.cur_top_card, player_turn=cur_player == player_1):
                    card.update_image()

                    if card.value != 13 and card.value != 14:
                        main_board.put_card_on_top(card)
                        player_1.hand.remove(card)
                        player_1.update_card_positions()
                        main_player_picked_something = True
                        break
                    else:
                        put_card_on_top_after_color_choice = card
                        break
            
            # if player_turn
            if cur_player == player_1 and not main_player_draw_a_card:
                if cur_mouse_x >= deck_card_x and cur_mouse_y >= deck_card_y and cur_mouse_x <= (deck_card_x + card_width) and cur_mouse_y <= (deck_card_y + card_height):
                    player_1.draw_cards(1)
                    main_player_draw_a_card = True
                    put_card_on_top_after_color_choice = None
                    dack_back_uno_card = pygame.image.load('card_images/uno_cover.png')

            if main_player_picked_something:
                reset_player_1_status()
                main_board.next_player()
    
    #display and add listener to skip turn button
    if main_player_draw_a_card:
        skip_button.listen(events)
        skip_button.draw()

    #display pick color buttons if necessarry
    if put_card_on_top_after_color_choice != None:
        pick_color_red.listen(events)
        pick_color_red.draw()
        pick_color_green.listen(events)
        pick_color_green.draw()
        pick_color_blue.listen(events)
        pick_color_blue.draw()
        pick_color_yellow.listen(events)
        pick_color_yellow.draw()
    
    #put card on top after player color choice
    if put_card_on_top_after_color_choice != None and player_1.chosen_color != None:
        main_board.put_card_on_top(put_card_on_top_after_color_choice, color_if_change_color=player_1.chosen_color)
        player_1.hand.remove(put_card_on_top_after_color_choice)
        player_1.update_card_positions()

        reset_player_1_status()
        main_board.next_player()

    #if bot plays
    if cur_player != player_1:
        main_board.make_bot_move()


    #display card in the middle
    display_up_card(card_on_middle_x, card_on_middle_y, main_board.cur_top_card)

    #display deck card in the middle
    gameDisplay.blit(dack_back_uno_card, (deck_card_x, deck_card_y))

    #display bot player information
    player_infos = main_board.get_bot_players_info()
    
    for i, player_info in enumerate(player_infos):
        cur_bot_display_info = 'Bot player ' + str(i + 1) + ': ' + str(player_info) + ' cards'
        textsurface = myfont.render(cur_bot_display_info, True, (0, 0, 0))
        gameDisplay.blit(textsurface, (0, 30 * i))

        if player_info == 1:
            cur_bot_one_card_display_info = 'Bot player ' + str(i + 1) + ' has only one card left!'
            textsurface_one_card = myfont.render(cur_bot_one_card_display_info, True, (255, 0, 0))
            gameDisplay.blit(textsurface_one_card, (display_width / 2.0 - 160, display_height / 2.0 + 80 + 20*i))

    #display current player
    if main_board.cur_player == 0:
        cur_player_text = "It's your turn"
    else:
        cur_player_text = "It player " + str(main_board.cur_player) + " turn"
    textsurface = myfont.render(cur_player_text, True, (0, 0, 255))
    gameDisplay.blit(textsurface, (display_width / 2.0 - 55, display_height / 2.0 - 200))

    #display cur card color
    if main_board.cur_top_card.color == 'red':
        color = (255, 0, 0)
    elif main_board.cur_top_card.color == 'green':
        color = (0, 255, 0)
    elif main_board.cur_top_card.color == 'blue':
        color = (0, 0, 255)
    elif main_board.cur_top_card.color == 'yellow':
        color = (255, 255, 0)
    textsurface = myfont.render(main_board.cur_top_card.color, True, color)
    gameDisplay.blit(textsurface, (display_width / 2.0 - 14, 10))

    #check for victory
    game_running = main_board.check_for_victory()

    pygame.display.update()

    clock.tick(FPS)

pygame.quit()
quit()