import cv2 as cv
import numpy as np
import scipy.optimize as optimize
from matplotlib import pyplot as plt

#read in file
path = "/Users/sanjayrajmurali/Documents/Python/red.png"
img = cv.imread(path)

#flips color channels to HSV & RGB
img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
img_hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

#show picture
plt.subplot(1, 1, 1)
plt.imshow(img_rgb)
plt.show()

#defining color thresholds
img_thresh_low = cv.inRange(img_hsv, np.array([0, 135, 135]), np.array([15, 255, 255]))
img_thresh_high = cv.inRange(img_hsv, np.array([159, 135, 135]), np.array([179, 255, 255]))

#combines thresholds
img_thresh = cv.bitwise_or(img_thresh_low, img_thresh_high) 

#erode and dilate using 5x5 kernel to remove noise 
kernel = np.ones((5, 5))
img_thresh_opened = cv.morphologyEx(img_thresh, cv.MORPH_OPEN, kernel)

#blurs image
img_thresh_blurred = cv.medianBlur(img_thresh_opened, 5)

#finds edges and then gets the contours
img_edges = cv.Canny(img_thresh_blurred, 70, 255)
contours, _ = cv.findContours(np.array(img_edges), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
img_contours = np.zeros_like(img_edges)

#places contours on new image
cv.drawContours(img_contours, contours, -1, (255,255,255), 2)

#simplifies contours based on Douglas-Peucker algorithm
approx_contours = []
for c in contours:
    approx = cv.approxPolyDP(c, 10, closed = True)
    approx_contours.append(approx)
img_approx_contours = np.zeros_like(img_edges)
cv.drawContours(img_approx_contours, approx_contours, -1, (255,255,255), 1)

#finds convex hulls
all_convex_hulls = []
for ac in approx_contours:
    all_convex_hulls.append(cv.convexHull(ac))
img_all_convex_hulls = np.zeros_like(img_edges)
cv.drawContours(img_all_convex_hulls, all_convex_hulls, -1, (255,255,255), 2)

#makes sure the only hulls are the ones between 3 and 10 points
convex_hulls_3to10 = []
for ch in all_convex_hulls:
    if 3 <= len(ch) <= 10:
        convex_hulls_3to10.append(cv.convexHull(ch))
img_convex_hulls_3to10 = np.zeros_like(img_edges)
cv.drawContours(img_convex_hulls_3to10, convex_hulls_3to10, -1, (255,255,255), 2)

#function to determine hull is pointing up
#finds the middle horizantal line and splits up the points into top and bottom ones 
#returns a boolean that represents whether all of the top points have x-values that are between the most extreme x-values of the bottom points

def convex_hull_pointing_up(ch):
    points_above_center, points_below_center = [], []
    x, y, w, h = cv.boundingRect(ch)
    aspect_ratio = w / h 
    if aspect_ratio < 0.8:
        vertical_center = y + h / 2
        for point in ch:
            if point[0][1] < vertical_center:
                points_above_center.append(point)
            elif point[0][1] >= vertical_center:
                points_below_center.append(point)
        left_x = points_below_center[0][0][0]
        right_x = points_below_center[0][0][0]
        for point in points_below_center:
            if point[0][0] < left_x:
                left_x = point[0][0]
            if point[0][0] > right_x:
                right_x = point[0][0]
        for point in points_above_center:
            if (point[0][0] < left_x) or (point[0][0] > right_x):
                return False
    else:
        return False
    return True

#determines if contour is cone and transcibes into rectangle
cones = []
bounding_rects = []
for ch in convex_hulls_3to10:
    if convex_hull_pointing_up(ch):
        cones.append(ch)
        rect = cv.boundingRect(ch)
        bounding_rects.append(rect)

#eliminates contours not pointing up
img_cones = np.zeros_like(img_edges)
cv.drawContours(img_cones, cones, -1, (255,255,255), 2)
img_res = img_rgb.copy()
cv.drawContours(img_res, cones, -1, (255,255,255), 2)
for rect in bounding_rects:
    cv.rectangle(img_res, (rect[0], rect[1]), (rect[0]+rect[2], rect[1]+rect[3]), (1, 255, 1), 3)

#function that uses least squares to get the parameters for a best fit line
def least_squares(x, y):
    def func(x, a, b):
        return a * x + b
    popt, pcov = optimize.curve_fit(func, x, y)
    return popt
img_out = img_rgb.copy()

#gets the points on the left and right sides
cone_points_left = [(rect[0] + rect[2]/2, rect[1] + rect[3]/2) for rect in bounding_rects if rect[0] + rect[2]/2 < img_res.shape[1]/2]
cone_points_right = [(rect[0] + rect[2]/2, rect[1] + rect[3]/2) for rect in bounding_rects if rect[0] + rect[2]/2 > img_res.shape[1]/2]

#gets best fit lines for these points
a1, b1 = least_squares(np.array([i[0] for i in cone_points_left]), np.array([i[1] for i in cone_points_left]))
a2, b2 = least_squares(np.array([i[0] for i in cone_points_right]), np.array([i[1] for i in cone_points_right]))

#creates & saves final output as png image
cv.line(img_out, [0, int(b1)], [3000, int((3000 * a1) + b1)], (255,1,1), 5)
cv.line(img_out, [0, int(b2)], [3000, int((3000 * a2) + b2)], (255,1,1), 5)
plt.imshow(img_out)
plt.savefig("answer.png")
plt.show()