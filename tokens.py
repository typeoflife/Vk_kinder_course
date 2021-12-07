def vktoken():
    with open('vktoken.txt') as file:
        vktoken = file.read().strip()
        return vktoken

def vkbottoken():
    with open('vkbot.txt') as file:
        vkbottoken = file.read().strip()
        return vkbottoken