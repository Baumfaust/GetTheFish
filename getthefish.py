import pyscreenshot as ImageGrab
import time
import pyautogui
import random
import jsonpickle

startPos = (200, 50)
endPos = (1100, 400)

offset = (0,-5)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def checkColor(color1, color2, delta):
    if ((color2[0]-delta <= color1[0] <= color2[0]+delta)
        and (color2[1]-delta <= color1[1] <= color2[1]+delta)
        and (color2[2]-delta <= color1[2] <= color2[2]+delta)):
        return True
    else:
        return False


class FishConfig():
    def __init__(self):
        self.jumpToBobber = True
        self.verbose = False
        self.thresholdBobber = 18
        self.thresholdCatch = 60
        self.bobbercolor = (72, 41, 12)


class GetTheFish():
    def __init__(self):
        pyautogui.FAILSAFE = False
        self.run = True
        self.gui = False
        self.fishConfig = FishConfig()
        #self.save()
        self.load()
        print("init "+ str(self.fishConfig.jumpToBobber))

    def save(self):
        with open('config.json', 'w') as file:
            file.write(jsonpickle.encode(self.fishConfig))

    def load(self):
        with open('config.json', 'r') as file:
            content = file.read()
            self.fishConfig = jsonpickle.decode(content)

    def log(self, text):
        if self.verbose:
            print(text)

    def findbobber(self):
        self.log("Searching for bobber")
        image = ImageGrab.grab()
        image.save("test.png")
        for y in range(startPos[1], endPos[1]):
            for x in range(startPos[0], endPos[0]):
                color = image.getpixel((x, y))
                if checkColor(color, self.fishConfig.bobbercolor, self.fishConfig.thresholdBobber):
                    end = time.time()
                    self.log("Bobber found at position: " + str(x) + ", " + str(y))
                    return Point(x, y)
        self.log("Bobber not found")
        return None

    def waitforFish(self, bobberPos):
        start = time.time()
        fishtime = 0
        oldx = oldy = 0
        image = ImageGrab.grab(bbox=(bobberPos.x, bobberPos.y, bobberPos.x + 1, bobberPos.y + 1))
        colorPosition = image.getpixel((0, 0))

        while (fishtime < 20):
            image = ImageGrab.grab(bbox=(bobberPos.x, bobberPos.y, bobberPos.x + 1, bobberPos.y + 1))
            color = image.getpixel((0, 0))
            if not checkColor(color, colorPosition, self.fishConfig.thresholdCatch):
                time.sleep(random.uniform(0.2, 0.9))
                pyautogui.position(oldx, oldy)
                pyautogui.moveTo(bobberPos.x, bobberPos.y)
                pyautogui.click(button='right')
                pyautogui.moveTo(oldx, oldy)
                return True
            fishtime = time.time() - start
        return False

    def fishing(self):
        while (self.run):
            self.save()
            pyautogui.moveTo(startPos[0], startPos[1])
            # pyautogui.press('1')
            pyautogui.click(button='right')
            pyautogui.click(button='right')
            wait = random.uniform(2.1, 2.9)
            self.log("Start fishing in " + str(round(wait, 1)) + " seconds")
            time.sleep(wait)
            bobberPos = self.findbobber()

            if bobberPos != None:
                bobberPos.x = bobberPos.x + 3
                bobberPos.y = bobberPos.y + 5
                pyautogui.moveTo(bobberPos.x, bobberPos.y)
                # sys.exit(0)
                self.log("Wait for Fish")
                caught = self.waitforFish(bobberPos)
                if caught:
                    self.log("Fish!")
                else:
                    self.log("Fish gone!")

                time.sleep(2)


if __name__ == '__main__':
    #bobbercolor = (105,108,127)

    # time.sleep(5)
    # pos = pyautogui.position()
    # print(pos)
    # time.sleep(2)
    # pyautogui.moveTo(pos[0], pos[1])
    # time.sleep(2)
    # image = ImageGrab.grab()
    # color = image.getpixel((pos[0], pos[1]))
    # print(color)
    # sys.exit(0)

    time.sleep(3)
    pyautogui.moveTo(startPos[0], startPos[1])
    time.sleep(2)
    pyautogui.moveTo(endPos[0], endPos[1])
    pyautogui.moveTo(endPos[0], endPos[1])
    time.sleep(2)




