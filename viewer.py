from PyQt5.QtWidgets import QMainWindow, QOpenGLWidget, QAction, QFileDialog, QLabel
from PyQt5.QtCore import Qt
from OpenGL.GL import *
from OpenGL.GLU import *
from file_loader import load_ifc_file
# from geometry_utils import highlight_wall, get_wall_properties

class BIMViewer(QOpenGLWidget):
    def __init__(self):
        super().__init__()
        self.shapes = []
        self.rotation = [0, 0, 0]
        self.translation = [0, 0, -50]
        self.selected_wall = None#
        self.info_label = QLabel(self)#

    def initializeGL(self):
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        
        # 4 Direction and negatives
        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_POSITION, (1, 1, 1, 0))
        
        glEnable(GL_LIGHT1)
        glLightfv(GL_LIGHT1, GL_POSITION, (-1, 1, 1, 0))
        
        glEnable(GL_LIGHT2)
        glLightfv(GL_LIGHT2, GL_POSITION, (1, -1, 1, 0))
        
        glEnable(GL_LIGHT3)
        glLightfv(GL_LIGHT3, GL_POSITION, (-1, -1, -1, 0))
        
        glEnable(GL_LIGHT4)
        glLightfv(GL_LIGHT4, GL_POSITION, (0, 0, 1, 0))  # Top light
        
        glEnable(GL_LIGHT5)
        glLightfv(GL_LIGHT5, GL_POSITION, (0, 0, -1, 0)) # Bottom light

        glEnable(GL_COLOR_MATERIAL)
        glShadeModel(GL_SMOOTH)
        glEnable(GL_CULL_FACE)

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, w/h, 0.1, 1000.0)

    def draw_axis(self):
        
        glDisable(GL_LIGHTING)

        # Draw X-axis in red
        glColor3f(1.0, 0.0, 0.0)
        glBegin(GL_LINES)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(10.0, 0.0, 0.0)
        glEnd()

        # Draw Y-axis in green
        glColor3f(0.0, 1.0, 0.0)
        glBegin(GL_LINES)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(0.0, 10.0, 0.0)
        glEnd()

        # Draw Z-axis in blue
        glColor3f(0.0, 0.0, 1.0)
        glBegin(GL_LINES)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(0.0, 0.0, 10.0)
        glEnd()

    def paintGL(self):

        glClearColor(1.0, 1.0, 1.0, 1.0) #change background to white
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
       
        self.translation = [0, -10, -50]
    
        glTranslatef(*self.translation)
        glRotatef(self.rotation[0], 1, 0, 0)
        glRotatef(self.rotation[1], 0, 1, 0)
        
        for shape in self.shapes:
            self.draw_shape(shape)

        # Draw axis
        self.draw_axis()

    def draw_shape(self, shape):
        if shape and shape.geometry:
            verts = shape.geometry.verts
            faces = shape.geometry.faces

            
            glColor4f(0.6, 0.6, 0.8, 0.5)  
            glBegin(GL_TRIANGLES)
            for i in range(0, len(faces), 3):
                for j in range(3):
                    idx = faces[i + j] * 3
                    glVertex3f(verts[idx], verts[idx + 1], verts[idx + 2])
            glEnd()

            
            glColor3f(0.2, 0.2, 0.2)  
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            glBegin(GL_TRIANGLES)
            for i in range(0, len(faces), 3):
                for j in range(3):
                    idx = faces[i + j] * 3
                    glVertex3f(verts[idx], verts[idx + 1], verts[idx + 2])
            glEnd()
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    def mousePressEvent(self, event):
        self.last_pos = event.pos()

    def mouseMoveEvent(self, event):
        dx = event.x() - self.last_pos.x()
        dy = event.y() - self.last_pos.y()

        if event.buttons() & Qt.LeftButton:
            self.rotation[1] += dx
            self.rotation[0] += dy
        elif event.buttons() & Qt.RightButton:
            self.translation[0] += dx * 0.1
            self.translation[1] -= dy * 0.1

        self.last_pos = event.pos()
        self.update()

    def wheelEvent(self, event):
        self.translation[2] += event.angleDelta().y() * 0.1
        self.update()

    
class MainWindow(QMainWindow):
    def __init__(self):
       super().__init__()
       self.setWindowTitle("IFC Viewer")
       
       open_action = QAction("Open IFC File", self)
       open_action.triggered.connect(self.open_file)

       menu_bar = self.menuBar()
       file_menu = menu_bar.addMenu("File")
       file_menu.addAction(open_action)

       self.viewer = BIMViewer()
       self.setCentralWidget(self.viewer)

    def open_file(self):
       filename, _ = QFileDialog.getOpenFileName(self, "Open IFC File", "", "IFC Files (*.ifc)")
       if filename:
           shapes = load_ifc_file(filename)
           if shapes:
               self.viewer.shapes = shapes
               self.viewer.update()