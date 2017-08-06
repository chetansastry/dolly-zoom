# Dolly zoom without Zoom lens

Dolly zoom (or the Vertigo effect) is an in-camera effect that is used in dramatic scenes to make the background 
appear collapsing on a foreground subject. See examples [here](https://www.youtube.com/watch?v=u5JBlwlnJX0).

This effect is usually achieved by employing a zoom lens on a camera mounted on the dolly and gradually moving the
camera away from a subject while zooming in (or the other way around) so that the subject remains the same size whereas
the background undergoes [Perspective distortion](https://en.wikipedia.org/wiki/Perspective_distortion_(photography)).

The technique used in this project employs a simple cellphone camera without a zoom lens and tries to get the same results
by means of cropping instead of zooming. Given the high-resolution of the contemporary cellphone camera, an image can be
cropped to a fraction of its original size while still maintaining a decent quality even at 1080p.

This project was done as part of the final project for
[CS6475: Computational Photography](https://www.omscs.gatech.edu/cs-6475-computational-photography) at Georgia Institute of 
Technology.

![](https://github.com/chetansastry/dolly-zoom/raw/master/demo.gif)

## Dependencies

* Python 2.7
* Numpy
* OpenCV

## Usage

Run main.py for usage information

## Credits and references

1. Motivation - https://petapixel.com/2016/10/11/create-dolly-zoom-effect-post-no-zoom-lens-required/
2. The amazing teaching staff at The Georgia Institute of Technology
