from gaitXYPoints import trajectory
import numpy as np
import ikpy.link
import ikpy.chain
import ikpy


hipLeg = ikpy.link.Link("hipLeg", 7)
kneeLeg = ikpy.link.Link("kneeLeg", 13)

hipLeg.has_rotation = True
kneeLeg.has_rotation = True

armRep = ikpy.chain.Chain([hipLeg, kneeLeg], [True, True], 'armChain')

point = [0,-20,0]
print(armRep.inverse_kinematics(point))

points = []
angles = []

L1 = 7
L2 = 13

def processTrajectory():
    trajectoryNewLineSplit = trajectory.split('\n')
    for line in trajectoryNewLineSplit:
        point = line.split(" ")
        if(len(point) != 1):
            points.append({"pointX":float(point[0]), "pointY":float(point[1])})

def pointToAngle(pointX, pointY):
  L3 = ((pointX**2) + (pointY**2))**(1 / 2)
  
  if(L2 > L3):
    phi1 = np.arctan2(pointY,pointX)
    #   print((L2**2 - L1**2 - L3**2) / (-2*L1*L3))

    alpha2 = np.arccos((L2**2 - L1**2 - L3**2) / (-2*L1*L3))

    theta1 = np.pi - phi1 - alpha2

    #   print((L3**2 - L1**2 - L2**2) / (-2*L1*L2))
    alpha3 = np.arccos((L3**2 - L1**2 - L2**2) / (-2*L1*L2))
    theta2 = np.pi - alpha3 
  else:
     alpha3 = np.arccos((L3**2 - L1**2 - L2**2) / (-2*L1*L2))
     theta2 = np.pi - alpha3

     alpha2 = np.arccos((L2**2 - L1**2 - L3**2) / (-2*L1*L3))
     phi1 = np.arctan2(pointY, pointX)

     theta1 = phi1 - alpha2
     
  
  theta1 = np.rad2deg(theta1)
  theta2 = np.rad2deg(theta2)
#   print("\n")
  
  angles.append({"theta1":theta1, "theta2":theta2})

processTrajectory()
for coords in points:
  pointToAngle(coords["pointX"], coords["pointY"])

for i in range(0, len(points)):
   print(str(points[i]) + ": " + str(angles[i]))