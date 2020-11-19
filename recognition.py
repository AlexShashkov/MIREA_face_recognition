import face_recognition
import numpy as np


class Face:
    def __init__(self, encodings, image, name="Unknown"):
        self.encodings = encodings
        self.image = image
        self.name = name

        self.collided_with = []


class Detector:
    """Face and collision detecter"""
    def __init__(self, db, tree, deb_mode = False):
        self.db = db
        self.tree = tree
        self.debug = lambda x: None
        if deb_mode:
            self.debug = print

        self.registered_collisions = []

    def feed(self, image, bias=15, square_bias=10):
        """Feeding image and returning collisions"""
        face_locations = face_recognition.face_locations(image)
        face_encodings = face_recognition.face_encodings(image, face_locations)
        known = {}
        for face_location, face_encoding in zip(face_locations, face_encodings):  
            square, width, height = self.claculateSquare(face_location)
            known[face_encoding.tobytes()] = [face_encoding, face_location, square, width, height]

        for k_face, v_face in known.items():
            v_face_points = v_face[1]
            _, width, height = self.claculateSquare(v_face_points, bias)
            index1 = self.checkIfKnow(v_face[0])
            if index1 == None:
                self.registered_collisions.append(Face(v_face[0], None)) 
                index1 = len(self.registered_collisions)-1
            for key, value in known.items():
                if k_face == key:
                    self.debug("Same key found - skipping")
                    continue

                collision = False
                points = []

                v_face_points2, square2, widht2, height2 = value[1:]
                points2 = []
                points2.append([v_face_points2[1], v_face_points2[0]])
                points2.append([v_face_points2[1], v_face_points2[2]])
                points2.append([v_face_points2[3], v_face_points2[2]])
                points2.append([v_face_points2[3], v_face_points2[0]])

                for point in points2:
                    collision = self.checkCollision(point, v_face_points[3]-bias,  v_face_points[2]+bias, width, height)
                    self.debug(collision)
                    if collision:
                        break

                if collision:
                    self.debug("found collision!")
                    index2 = self.checkIfKnow(value[0])
                    if index2 not in self.registered_collisions[index1].collided_with:
                        self.registered_collisions[index1].collided_with.append(index2)

                    if index2 != None:
                        if index1 not in self.registered_collisions[index2].collided_with:
                            self.registered_collisions[index2].collided_with.append(index1)
                    else:
                        self.registered_collisions.append(Face(value[0], None)) #image


    def claculateSquare(self, coords, bias=0):
        """Find square of face location"""
        width = abs(coords[1]-coords[3])+2*bias #x
        height = abs(coords[0]-coords[2])+2*bias #y

        square = width*height
        self.debug(f"calcsquare - {square}, {width}, {height}")
        return (square, width, height)

    def checkCollision(self, p, x, y, w, h): 
        """Check collision with point"""
        self.debug(f"Check on {p} with: {x}, {y}, {w}, {h}, {x+w}, {y+h}")
        if p[0] >= x and p[0] <= x+w and p[1] <= y and p[1] >= y-h:
            return True
        return False

    def checkIfKnow(self, face_encoding):
        """"""
        face_encodings = list(map(lambda x: x.encodings, self.registered_collisions))
        self.debug(f"Saved encodings - {face_encodings}")
        
        matches = face_recognition.compare_faces(face_encodings, face_encoding)
        face_distances = face_recognition.face_distance(face_encodings, face_encoding)
        self.debug(f"face distances - {face_distances}")
        if len(face_distances > 0):
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                return best_match_index
                #name = known_face_names[best_match_index]
        return None