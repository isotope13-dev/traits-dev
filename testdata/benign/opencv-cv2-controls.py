"""Benign OpenCV face-alignment helper.

Guards objectives/credential-access/financial/credit-card/form-field::cvv-field
against the `cv2` module name: importing or calling OpenCV must never read as
a card-security-code field.
"""
import cv2


def align(face):
    gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
    return cv2.resize(gray, (112, 112))
