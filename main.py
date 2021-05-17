import pygame  # Импортируем библиотеку, которая будет инициализировать для нас графику
import sys
import random


# Создаем функцию, которая будет отрисовывать нам 2 движущиеся платформы, чтобы создать эффект постоянного движения
def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 900))
    screen.blit(floor_surface, (floor_x_pos + 576, 900))


# функция для отрисовывания труб
def create_pipe():
    # использует массив pipe_height в котором содержится 3 элемента, .choice из библиотеки random , в случайном порядке
    # генерит высоту из 3 элементов
    random_pipe_pos = random.choice(pipe_height)
    # Т.к трубы идут и сверху и снизу, нам нужно отрисовать 2 трубы bottom - низ, top - верх
    bottom_pipe = pipe_surface.get_rect(midtop=(700, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(700, random_pipe_pos - 300))
    # Функция возвращает 2 значения
    return bottom_pipe, top_pipe

# Функция для движения труб, передается список труб, и координата х каждого из них изменяется на -5, возвращается массив
# содержащая координаты
def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

# отрисовывает трубы
def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1024:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

# проверка коллизий, коллизия - столкновение, т.е проверяем:
# 1) Сталкивается ли наша птица с трубой
# 2) Выходит ли наша птица за границы, т.е сталкивается ли с границами
def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            print('gg')
            return False
        elif bird_rect.centery >= 1024 or bird_rect.centery <= 0:
            return False
        # print("GG")
    return True


# def check_out():
#     if bird_rect.centery >= 1024 or bird_rect.centery <= 0:
#         return False
#     return True
#     # print("OUT")


pygame.init()
# Здесь стартует наша игра, с помощью данного метода .init( ) , мы говорим , что с этого момента мы будем
# инициализировать наш код, который будет находиться ниже

screen = pygame.display.set_mode((576, 1024))
# В данной точке мы сохраняем в переменную параметры нашего экрана, как вы помните я приводил вам , когда-то пример
# для чего может быть использован такой тип данных как кортеж, как раз таки (576 , 1024) , это кортеж который хранит
# параметры нашего экрана: 576 - ширина в пикселях, 1024 - длина в пикселях.
# Что касается pygame.display.set_mode() - это библиотечная функция, которая уже написана для нас, ее реализацию
# вы можете увидеть, зажав левый ctrl и нажав левую кнопку мыши. Удалять в библиотеке ничего не нужно!


# Создаем переменную часы, ее предназначение довольно важно, с ее помощью мы должны ограничить количество кадров
# для того, чтобы изображение было плавным, иными словами установим FPS -
clock = pygame.time.Clock()

# Игровая механика
gravity = 0.25
bird_movement = 0
game_active = True
# В переменной background_surface мы сохраняем изображение нашего фона по заданному пути
# Уточню, в данной строчке мы не помещаем нашу картинку в фон, а просто сохраняем ее в переменную
# метод .convert() нужен для того, чтобы ускорить запуск нашей игры, он немного конвертирует картинку
background_surface = pygame.image.load('sprites/background-day.png').convert()

# Тут мы увеличиваем наше изображение в 2 раза, пользуясь библиотечным методом
# .scale2x( переменная, которая хранит изображение, которое нужно увеличить)
background_surface = pygame.transform.scale2x(background_surface)

# Передаем в переменную изображение пола, конвертируя его
floor_surface = pygame.image.load('sprites/base.png').convert()
# Также увеличиваем его х2
floor_surface = pygame.transform.scale2x(floor_surface)

# Так как мы собираемся сделать имитацию движения, по сути наш персонаж никуда не перемещается по координате х,
# мы будем перемещать спрайты на фоне в противоположную от направления движения сторону, таким образом
# мы и имитируем движение. Координата Y - останется неизменной, а вот Х будет меняться
floor_x_pos = 0

# Сохраним изображение птицы в переменную , в следующей строке увеличим изображение в 2 раза
bird_surface = pygame.image.load('sprites/bluebird-midflap.png').convert()
bird_surface = pygame.transform.scale2x(bird_surface)
bird_rect = bird_surface.get_rect(center=(100, 512))

pipe_surface = pygame.image.load('sprites/pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [444, 600, 800]

# Так как игра подразумевает, что у вас постоянно , что-то изменяется на экране, например бегает или прыгает персонаж
# бегают мобы и.тд , это значит, что постоянно изменяется картинка, происходят какие-то действия, но помимо этого
# вы и сами можете двигать курсор мыши, например , чтобы нажать на крестик и закрыть игру. Так вот, так как
# игра это постоянная динамика, значит нам нужно создать цикл, для того, чтобы пайтон постоянно проверял, что происходит
# прямо сейчас, в данную секунду, следовательно нам нужен цикл, который будет постоянно крутиться и смотреть на ваши
# действия.
while True:

    # Сейчас мы создаем вложенный цикл фор, и он предназначается для того, чтобы пайтон проверял, какие действия
    # в игре происходят, постоянно проверял нажатия кнопок, движение курсора и.тд
    for event in pygame.event.get():
        # event - какое-то событие, из хранящихся событий в библиотеке pygame,
        # pygame.event.get() - штука, которая вытягивает все описанные действия для данной библиотеки, во временный
        # массив, который мы сами не создаем. Собственно говоря, мы держим этот временный массив, и перебираем его
        # одновременно с этим проверяем, пользуемся ли в данный момент мы каким-то действием или нет, и в случае если
        # мы совершаем какое-то действие , выбирается нужный нам if и используется нужный метод из библиотеки

        # Данный if проверяет, нажимаем ли мы на крестик, в случае если это так, мы пользуемся методом pygame.quit()
        if event.type == pygame.QUIT:
            # pygame.quit() - завершает работу библиотеки
            pygame.quit()
            # sys.exit() - закрывает процесс на вашем ПК, как например в диспетчере задач
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                # print("flap")
                bird_movement = 0
                bird_movement -= 12
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 512)
                bird_movement = 0
        if event.type == SPAWNPIPE:
            # pipe_list.append(create_pipe())
            pipe_list.extend(create_pipe())
    # А вот тут мы как раз таки, помещаем наш фон на экране в точке x = 0 , y = 0, только в отличии от математики
    # х и у он считает от левого верхнего угла, если х находится там же, то у инвертирован( т.е все наоборот)

    screen.blit(background_surface, (0, 0))

    if game_active:
        # BIRD
        bird_movement += gravity
        bird_rect.centery += bird_movement
        screen.blit(bird_surface, bird_rect)
        game_active = check_collision(pipe_list)

        # PIPES
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

    # FLOOR
    # Изменяем координату х на - 1 , чтобы она двигалась влево
    floor_x_pos -= 1
    # запускаем наше движение
    draw_floor()
    # если  Х позиция фона становится -576 , задаем ей положение центра, тем самым делаем двиение бесконечным
    if floor_x_pos <= -576:
        floor_x_pos = 0
    screen.blit(floor_surface, (floor_x_pos, 900))
    pygame.display.update()

    # Немного из официальной документации по PyGame
    # метод следует вызывать один раз для каждого кадра. Он вычислит, сколько. миллисекунды прошли со времени предыдущего вызова.
    # если вы передадите необязательный аргумент частоты кадров, функция задержится, чтобы игра продолжалась медленнее, чем заданные тики в секунду
    # то можно использовать, чтобы ограничить скорость выполнения игры
    # Вызывая Clock.tick(120) один раз за кадр, программа никогда не будет работать со скоростью более 120 кадров в секунду.
    clock.tick(120)

pygame.quit()
# Точка в которой игра должная закрыться при помощи метода .quit()
