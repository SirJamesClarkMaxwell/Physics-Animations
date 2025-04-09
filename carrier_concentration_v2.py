from manimlib import *
def get_camera_position(scene:Scene):
    print(f"{scene.frame.camera_location=}")
    print(f"{scene.frame.get_euler_angles()=}")


class TranslusiveRectangle(VGroup):
    def __init__(self, width:float, height:float, n_steps:int,
                start_color, end_color=BLACK, 
                opacity:float=1, direction=UP,
                *args, **kwargs):
        super().__init__(*args, **kwargs)
        strips = []
        for i in range(n_steps):
            alpha = i / n_steps
            step_opacity = max(opacity * (1 - alpha), 0)
            strip = Rectangle(
                height=height / n_steps,
                width=width,
                fill_color=interpolate_color(start_color, end_color, alpha),
                fill_opacity=step_opacity,
                stroke_width=0
            )
            strips.append(strip)
        self.add(*strips)
        self.arrange(direction, buff=0)

class Pointer(VGroup):
    def __init__(self,
                mobject:Mobject,
                label:str,
                line_direction=(UP+RIGHT),line_length:float=1,
                dot_size:float = 0.5,color=YELLOW,
                stroke_width:float=1,track:bool=False,*args,**kwargs):
        super().__init__(*args,**kwargs)        
        start_point = mobject.get_center()
        middle_point = start_point+line_direction*line_length
        
        text = TexText(fr"{label}")
        dot = Dot(dot_size if dot_size>0 else 0.5).move_to(mobject.get_center())
        first_line = Line(start=start_point,end=middle_point,stroke_width = stroke_width)
        
        text_width = text.get_width()
        second_line = Line(start=middle_point,end = middle_point+text_width*RIGHT,stroke_width = stroke_width)
        text.next_to(second_line,UP,SMALL_BUFF)
        super().add(dot,first_line,second_line,text).set_color(color)
        if track:
            self.add_updater(lambda mob: dot.move_to(mobject.get_center()))
            self.add_updater(lambda mob: first_line.become(Line(start=start_point,end=middle_point,stroke_width = stroke_width)))

class CarrierConcentrationV2(InteractiveScene):
    def construct(self) -> None:
        main_axes = Axes(x_range=[0, 5], y_range=[0, 6]).to_edge(LEFT,LARGE_BUFF)
        main_axes_coordinates = main_axes.add_coordinate_labels()
        # adding axes
        self.add(main_axes,main_axes_coordinates)
        x_label = main_axes.get_x_axis_label("x",X_AXIS,)
        E_label = main_axes.get_y_axis_label("E",Y_AXIS)
        cb,vb = self.get_bands(main_axes)
        self.add(x_label,E_label,cb,vb)
        
        ## add pointing animation for cb, vb
        
    
    def get_bands(self,axes:Axes,width:float = 3,height=1 ,Eg: float|ValueTracker=1.1):
        start_coord,end_coord = axes.c2p(0,0),axes.c2p(width,0,)
        Eg = Eg if type(Eg) is float else Eg.get_value()
        print(Eg)
        cb = axes.get_graph(
            lambda x: Eg, x_range=[0,width]
        )
        vb = axes.get_graph(
            lambda x: 0, x_range=[0,width]
        )
        conduction_band = TranslusiveRectangle(width = width,height=height,n_steps=50,start_color=BLUE).next_to(cb,UP,buff=0)
        valenced_band = TranslusiveRectangle(width = width,height=height,n_steps=50,start_color=RED,direction=DOWN).next_to(vb,DOWN,buff =0)
        return conduction_band,valenced_band
        
        
        
class Testing(InteractiveScene):
    def construct(self) -> None:
        s = Square()
        p = Pointer(s,"Square: Area = $a^2$",stroke_width=1,track=True)
        self.add(s)
        self.play(ShowCreation(p))
        self.play(s.animate.shift(LEFT))
        
        