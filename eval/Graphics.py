import numpy as np
import cv2

class Demo():


    def __init__(self):
        upArrow = np.array([ ( (270, 450), (270, 250) ), ( (350, 450), (350, 250) ), ( (430, 450), (430, 250) ) ])
        downArrow = np.array([ ( (270, 250), (270, 450) ), ( (350, 250), (350, 450) ), ( (430, 250), (430, 450) ) ])
        rightArrow = np.array([ ( (550, 270), (750, 270) ), ( (550, 350), (750, 350) ), ( (550, 430), (750, 430) ) ])
        leftArrow = np.array([ ( (750, 270), (550, 270) ), ( (750, 350), (550, 350) ), ( (750, 430), (550, 430) ) ])
        zoominArrow = np.array([ ( (330, 630), (230, 530) ), ((330, 670), (230, 770)  ), ( (370, 630), (470, 530) ), ((370, 670), (470, 770)  ) ])
        zoomoutArrow = np.array([ ((230, 530), (330, 630)  ), ( (230, 770), (330, 670) ), ( (470, 530), (370, 630) ), ((470, 770), (370, 670)  ) ])
        cwArrow = np.array( [ (0, 0), (0, 0) ] )
        ccwArrow = np.array( [ (0, 0), (0, 0) ] )
        frontSide = np.array([ ( (0, 0), (249, 50) ) ])
        rearSide = np.array([ ( (249, 249), (0, 200) ) ])
        leftSide = np.array([ ( (0, 50), (50, 200) ) ])
        rightSide = np.array([ ( (200, 50), (249, 200) ) ])
        #label =  "CW  FWD DWN RT CCW  BWD  UP  LFT oUP oLFT oRT oDWN mUP mLFT mRT mDWN iUP iLFT iRT iDWN C"
        #self.arrows = [ccwArrow, cwArrow, zoominArrow, zoomoutArrow, upArrow, downArrow, rightArrow, leftArrow, frontSide, rearSide, leftSide, rightSide]
        self.arrows = [cwArrow, zoominArrow, downArrow, rightArrow, ccwArrow, zoomoutArrow, upArrow, leftArrow, frontSide, rearSide, leftSide, rightSide]
        self.inactiveColor = (80, 80, 80)
        self.activeColor = (255, 255, 255)
        self.obstacleColor = (20, 200, 250)
        self.canvas = cv2.imread("assets/MotionBackground.jpg")
        self.blank = cv2.imread("assets/ObstacleBackground.jpg")

    def mountWindowAt(self, x, y):
        cv2.imshow("Motion", self.canvas)
        cv2.moveWindow("Motion", x, y)

    def drawArrows(self, image, positions, color):
        for index in range(positions.shape[0]):
            cv2.arrowedLine(image, tuple(positions[index][0]), tuple(positions[index][1]), color, thickness=20)
        return image

    def drawObstacles(self, image, locations, color):
        for index in range(locations.shape[0]):
            cv2.rectangle(image, tuple(locations[index][0]), tuple(locations[index][1]), color, thickness=cv2.FILLED)
        return image

    # front, rear, left, right
    def displayConfig(self, thresholds, config):
        motion = self.canvas.copy()

        for index, value  in enumerate(config):
            if index == 0:
                if value > thresholds[0]:
                    cv2.drawMarker(motion, (550, 650), self.activeColor, cv2.MARKER_TRIANGLE_UP, markerSize=50, thickness=20)
                    cv2.drawMarker(motion, (750, 650), self.activeColor, cv2.MARKER_TRIANGLE_DOWN, markerSize=50, thickness=20)
            elif index == 4:
                if value > thresholds[0]:
                    cv2.drawMarker(motion, (550, 650), self.activeColor, cv2.MARKER_TRIANGLE_DOWN, markerSize=50, thickness=20)
                    cv2.drawMarker(motion, (750, 650), self.activeColor, cv2.MARKER_TRIANGLE_UP, markerSize=50, thickness=20)
            elif index < 8:
                if value > thresholds[0]:
                    motion = self.drawArrows(motion, self.arrows[index], self.activeColor)

        if config[0] > thresholds[0] or config[4] > thresholds[0]:
            cv2.circle(motion, (650, 650), 100, self.activeColor, thickness=20)

        for index in range(8, 12):
            if config[index] > thresholds[1]:
                cv2.fillConvexPoly(motion, self.arrows[index], self.obstacleColor)

        cv2.imshow("Motion", motion)


class Flow():

    def __init__(self):
        None

    def display(self, frame, flow, fps):
        showFrame = frame.copy()
        showFrame = cv2.resize(showFrame, (512, 512))
        flow = flow.reshape(8, 8, 2)
        flow = cv2.resize(flow, (512, 512), cv2.INTER_NEAREST)
        for y in range(32, 512, 64):
            for x in range(32, 512, 64):
                cv2.line(showFrame, (x, y), (x+int(5*flow[y][x][0]), y+int(5*flow[y][x][1])), (255, 255, 255), 3)
        cv2.putText(showFrame, "FPS={:.1f}".format(fps), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (5, 255, 5))
        cv2.imshow("Flow", showFrame)

class Dot():

    def __init__(self):
        None

    def display(self, frame, label, flow, fps):
        showFrame = frame.copy()
        showFrame = cv2.resize(showFrame, (512, 512))
        interval = 40
        cv2.putText(showFrame, label[0:33], (15, 350), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255))
        cv2.putText(showFrame, "FPS={:.1f}".format(fps), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (5, 255, 5))
        for loc, val in enumerate(flow):
            cv2.line(showFrame, (25+loc*interval, 300), (25+loc*interval, 300-int(val*2)), color=(255, 55, 255), thickness=20)
        cv2.imshow("Dotted", showFrame)



