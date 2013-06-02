from direct.showbase import DirectObject
from pandac.PandaModules import Vec3,Vec2
from direct.task import Task


class TimCam(DirectObject.DirectObject):
    def __init__(self):
        base.disableMouse()
        self.camera_control()
        self.keyboard_setup()
        taskMgr.add(self.camera_update, "UpdateCameraTask")

    def camera_control(self):

        self.camera = base.camera

        self.cam_speed = 5
        self.cam_drag = 0.01

        self.cam_x_moving = False
        self.cam_y_moving = False
        self.cam_z_moving = False

        self.cam_x_inc = 0
        self.cam_y_inc = 0
        self.cam_z_inc = 5

        self.zoom_in = False
        self.zoom_out = False

        self.cameraDistance = -50
        self.camHeight = 25


        self.camXAngle = 0
        self.camYAngle = -90
        self.camZAngle = 0

        self.camX = 0
        self.camY = 0
        self.camZ = 500

    def camera_update(self,task):
        if self.zoom_in == True:
            self.camZ -= self.cam_z_inc
        if self.zoom_out == True:
            self.camZ += self.cam_z_inc

        if self.cam_x_moving:
            self.camX+=self.cam_x_inc
        elif self.cam_x_inc != 0:
            if (self.cam_x_inc > 0 and self.cam_x_inc-self.cam_drag <= 0) or (self.cam_x_inc < 0 and self.cam_x_inc+self.cam_drag >= 0):
                self.cam_x_inc = 0
            elif self.cam_x_inc > 0:
                self.cam_x_inc -= self.cam_drag
            elif self.cam_x_inc < 0:
                self.cam_x_inc -= self.cam_drag
            else:
                print "FUCKUP WITH CAM X INC"

        if self.cam_y_moving:
            self.camY+=self.cam_y_inc
        elif self.cam_y_inc != 0:
            if (self.cam_y_inc > 0 and self.cam_y_inc-self.cam_drag <= 0) or (self.cam_y_inc < 0 and self.cam_y_inc+self.cam_drag >= 0):
                self.cam_y_inc = 0
            elif self.cam_y_inc > 0:
                self.cam_y_inc -= self.cam_drag
            elif self.cam_y_inc < 0:
                self.cam_y_inc -= self.cam_drag
            else:
                print "FUCKUP WITH CAM Y INC"

        #if self.cam_z_moving:
        #    self.camZ+=self.cam_z_inc
        #elif self.cam_z_inc != 0:
        #    if (self.cam_z_inc > 0 and self.cam_z_inc-self.cam_drag <= 0) or (self.cam_z_inc < 0 and self.cam_z_inc+self.cam_drag >= 0):
        #        self.cam_z_inc = 0
        #    elif self.cam_z_inc > 0:
        #        self.cam_z_inc -= self.cam_drag
        #    elif self.cam_z_inc < 0:
        #        self.cam_z_inc -= self.cam_drag
        #    else:
        #        print "FUCKUP WITH CAM Z INC"

        self.camera.setPos(self.camX, self.camY, self.camZ)
        self.camera.setHpr(self.camXAngle, self.camYAngle, self.camZAngle)

        return Task.cont

    def camera_move(self, status):
        if status == "up":
            self.cam_y_moving = True
            self.cam_y_inc = self.cam_speed
        if status == "down":
            self.cam_y_moving = True
            self.cam_y_inc = -self.cam_speed
        if status == "left":
            self.cam_x_moving = True
            self.cam_x_inc = -self.cam_speed
        if status == "right":
            self.cam_x_moving = True
            self.cam_x_inc = self.cam_speed
        if status == "stopX":
            self.cam_x_moving = False
        if status == "stopY":
            self.cam_y_moving = False

    def keyboard_setup(self):
        self.accept("w", self.keyW)
        self.accept("w-up", self.stop_y)
        self.accept("s", self.keyS)
        self.accept("s-up", self.stop_y)
        self.accept("a", self.keyA)

        self.accept("a-up", self.stop_x)
        self.accept("d", self.keyD)
        self.accept("d-up", self.stop_x)
        self.accept("+", self.ZoomIn)
        self.accept("+-up", self.ZoomIn)
        self.accept("-", self.ZoomOut)
        self.accept("--up", self.ZoomOut)

    def ZoomIn(self):
        if self.zoom_in == True:
            self.zoom_in = False
        elif self.zoom_in == False:
            self.zoom_in = True

    def ZoomOut(self):
        if self.zoom_out == True:
            self.zoom_out = False
        elif self.zoom_out == False:
            self.zoom_out = True

    def keyW( self ):
        self.camera_move("up")

    def keyS( self ):
        self.camera_move("down")

    def keyA( self ):
        self.camera_move("left")

    def keyD( self ):
        self.camera_move("right")

    def stop_x( self ):
        self.camera_move("stopX")

    def stop_y( self ):
        self.camera_move("stopY")
