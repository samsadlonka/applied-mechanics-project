#!/usr/bin/env python

# This example creates a tube around a line.
# This is helpful because when you zoom the camera,
# the thickness of a line remains constant,
# while the thickness of a tube varies.


# noinspection PyUnresolvedReferences
import vtkmodules.vtkInteractionStyle
# noinspection PyUnresolvedReferences
import vtkmodules.vtkRenderingOpenGL2
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkFiltersCore import vtkTubeFilter
from vtkmodules.vtkFiltersSources import vtkLineSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer
)

ranges = [200 * i * 10 ** 6 for i in range(0, 7)]


def beams_colors(tensions):
    if not tensions:
        return None
    max_t = (int(str(max(tensions))[0]) + 1) * 10 ** (len(str(int(max(tensions)))) - 1)
    min_t = int(str(min(tensions))[0]) * 10 ** (len(str(int(min(tensions)))) - 1)
    step = (max_t - min_t) // 5
    color_list = []
    colors = ['blue', 'green', 'yellow', 'orange', 'red']
    for tension in tensions:
        i = 0
        if tension == max(tensions):
            color_list.append('black')
        else:
            while i < 4 and not (ranges[i] < tension < ranges[i + 1]):
                i += 1

            color_list.append(colors[i])
    return color_list


def draw(beams, tensions=None):
    colors = vtkNamedColors()
    colors.SetReferenceCount(2 ** 24)

    # Create a line
    lineSource = []
    for i in range(len(beams)):
        lineSource.append(vtkLineSource())
        lineSource[i].SetPoint1(*beams[i].get_points()[0])
        lineSource[i].SetPoint2(*beams[i].get_points()[1])

    # Setup actor and mapper
    lineMapper = []
    for i in range(len(beams)):
        lineMapper.append(vtkPolyDataMapper())
        lineMapper[i].SetInputConnection(lineSource[i].GetOutputPort())

    lineActor = []
    for i in range(len(beams)):
        lineActor.append(vtkActor())
        lineActor[i].SetMapper(lineMapper[i])
        lineActor[i].GetProperty().SetColor(colors.GetColor3d('Red'))

    # Create tube filter
    tubeFilter = []
    for i in range(len(beams)):
        tubeFilter.append(vtkTubeFilter())
        tubeFilter[i].SetInputConnection(lineSource[i].GetOutputPort())
        tubeFilter[i].SetRadius(0.025)
        tubeFilter[i].SetNumberOfSides(50)
        tubeFilter[i].Update()

    # Setup actor and mapper
    tubeMapper = []
    for i in range(len(beams)):
        tubeMapper.append(vtkPolyDataMapper())
        tubeMapper[i].SetInputConnection(tubeFilter[i].GetOutputPort())
    list_of_colors = beams_colors(tensions)

    tubeActor = []
    for i in range(len(beams)):
        tubeActor.append(vtkActor())
        tubeActor[i].SetMapper(tubeMapper[i])
        # Make the tube have some transparency.
        tubeActor[i].GetProperty().SetOpacity(0.5)
        if list_of_colors:
            tubeActor[i].GetProperty().SetColor(colors.GetColor3d(list_of_colors[i]))

    # Setup render window, renderer, and interactor
    renderer = vtkRenderer()
    renderWindow = vtkRenderWindow()
    renderWindow.SetPosition(300, 20)
    if tensions:
        renderWindow.SetWindowName('Ферма с напряжениями')
    else:
        renderWindow.SetWindowName('Ферма')
    renderWindow.AddRenderer(renderer)

    renderWindowInteractor = vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)
    # Visualise the arrow
    for i in range(len(beams)):
        lineActor[i].RotateX(-90)
        tubeActor[i].RotateX(-90)
        renderer.AddActor(lineActor[i])
        renderer.AddActor(tubeActor[i])

    renderer.SetBackground(colors.GetColor3d('DarkSlateGray'))
    renderer.ResetCamera()
    renderWindow.SetSize(600, 600)
    renderWindow.Render()
    renderWindowInteractor.Start()
