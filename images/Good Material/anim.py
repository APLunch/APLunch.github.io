# calibrate_rotating_pole.py
# Manim (3Blue1Brown style) animation for a 3-phase calibration workflow:
# Phase 1: camera-to-camera (master/slaves) using a gripper marker
# Phase 2: pole-axis identification by rotating the rig
# Phase 3: full BA-style optimization over robot J1 ↔ pole joint ↔ cameras
#
# Tested with Manim CE 0.17.x API (https://docs.manim.community/)
# Run one scene:
#   manim -pqh calibrate_rotating_pole.py MasterScene
# Or high quality:
#   manim -pqh calibrate_rotating_pole.py MasterScene --quality uhd_4k
#
# Notes:
# - This is an *illustrative* animation (not numerically accurate).
# - Replace placeholder geometry/labels with your project specifics as desired.

import numpy as np
from manimlib import *


# ---------- Small helper drawing utilities ----------

def camera_icon(color=BLUE, scale=0.6):
    body = RoundedRectangle(
        width=0.8, height=0.6, corner_radius=0.08,
        color=color, fill_opacity=0.9, stroke_width=2
    )
    lens_outer = Circle(radius=0.25, color=GREY_D, fill_opacity=1, stroke_width=2)
    lens_outer.shift(0.5*RIGHT)
    lens_inner = Circle(radius=0.18, color=color, fill_opacity=0.5, stroke_width=1)
    lens_inner.shift(0.5*RIGHT)
    lens_glare = Circle(radius=0.08, color=WHITE, fill_opacity=0.7, stroke_width=0)
    lens_glare.shift(0.5*RIGHT + 0.08*UP + 0.08*LEFT)
    viewfinder = Rectangle(width=0.15, height=0.12, color=GREY_C, fill_opacity=0.3, stroke_width=1)
    viewfinder.shift(0.25*LEFT + 0.2*UP)
    button = Circle(radius=0.05, color=RED, fill_opacity=0.8, stroke_width=1)
    button.shift(0.15*LEFT + 0.15*DOWN)
    g = VGroup(body, lens_outer, lens_inner, lens_glare, viewfinder, button).scale(scale)
    return g

def coordinate_frame(scale=0.4, origin=ORIGIN):
    x_axis = Arrow(origin, origin + scale*RIGHT, color=RED, buff=0, stroke_width=3)
    y_axis = Arrow(origin, origin + scale*UP, color=GREEN, buff=0, stroke_width=3)
    z_axis = Arrow(origin, origin + scale*OUT, color=BLUE, buff=0, stroke_width=3)
    x_label = Text("X", color=RED).scale(0.25).next_to(x_axis, RIGHT, buff=0.05)
    y_label = Text("Y", color=GREEN).scale(0.25).next_to(y_axis, UP, buff=0.05)
    z_label = Text("Z", color=BLUE).scale(0.25).next_to(z_axis, OUT, buff=0.05)
    return VGroup(x_axis, y_axis, x_label, y_label)

def checkerboard(rows=6, cols=9, square=0.18, color_1=WHITE, color_2=GREY_E):
    squares = VGroup()
    for r in range(rows):
        for c in range(cols):
            col = color_1 if (r + c) % 2 == 0 else color_2
            sq = Square(side_length=square, stroke_color=BLACK, stroke_width=1, fill_color=col, fill_opacity=1)
            sq.shift(((c - (cols-1)/2)*square, (r - (rows-1)/2)*square, 0))
            squares.add(sq)
    frame = Rectangle(width=cols*square, height=rows*square, stroke_color=BLACK, stroke_width=2)
    return VGroup(squares, frame)

def rig_mount():
    horizontal = Line(ORIGIN, 1.2*LEFT, color=GREY_B, stroke_width=12)
    vertical = Line(ORIGIN, 1.5*UP, color=GREY_B, stroke_width=12)
    vertical.move_to(horizontal.get_left(), aligned_edge=DOWN)
    joint = Circle(radius=0.08, color=GREY_C, fill_opacity=0.9, stroke_width=2)
    joint.move_to(horizontal.get_left())
    return VGroup(horizontal, vertical, joint)

def robot_base():
    base = RoundedRectangle(width=4.5, height=1.2, corner_radius=0.2, color=GREY_D, fill_opacity=0.6)
    label = Text("Robot Base (B)").scale(0.35).next_to(base, DOWN, buff=0.1)
    return VGroup(base, label)

def j1_axis():
    # Draw J1 as a rotating post at the base center
    disk = Circle(radius=0.28, color=GREY_D, fill_opacity=0.6)
    axis = Arrow(ORIGIN, 0.8*UP, buff=0, color=YELLOW)
    txt = Text("J1 (z)").scale(0.35).next_to(axis, UP, buff=0.05)
    return VGroup(disk, axis, txt)

def dashed_circle(center, radius, color=GREY_B):
    dots = VGroup()
    for a in np.linspace(0, TAU, 64):
        if int(a*10) % 2 == 0:
            p = center + radius*np.array([np.cos(a), np.sin(a), 0])
            dots.add(Dot(p, radius=0.007, color=color))
    return dots

def u_axis_arrow(point, direction, length=2.5, color=YELLOW):
    d = np.array(direction) / np.linalg.norm(direction)
    return Arrow(point - 0.5*length*d, point + 0.5*length*d, color=color, buff=0)

def brace_label(mobj, text, direction=DOWN, color=WHITE):
    br = Brace(mobj, direction=direction, color=color)
    lb = br.get_text(text).set_color(color)
    return VGroup(br, lb)

# ---------- Scene 1: Phase 1 (Camera-to-Camera calibration) ----------

class Phase1Scene(Scene):
    def construct(self):
        title = Tex(r"\textbf{Phase 1: Camera-to-Camera Calibration (rig fixed)}").to_edge(UP)
        self.play(FadeIn(title, shift=DOWN))

        # Layout
        base = robot_base().to_edge(DOWN, buff=0.3)
        j1 = j1_axis().next_to(base[0], UP, buff=0.1)

        rig = rig_mount()
        rig.move_to(j1.get_top() + 0.3*UP, aligned_edge=RIGHT)

        rig_top = rig[1].get_top()
        master = camera_icon(BLUE_E).move_to(rig_top + 0.3*DOWN + 0.2*LEFT)
        slave1 = camera_icon(GREEN_E).move_to(rig_top + 0.5*UP + 0.5*LEFT)
        slave2 = camera_icon(RED_E).move_to(rig_top + 0.5*UP + 0.1*RIGHT)

        master_label = Text("Master", color=BLUE_E).scale(0.35).next_to(master, RIGHT, buff=0.05)
        s1_label = Text("Slave A", color=GREEN_E).scale(0.35).next_to(slave1, LEFT, buff=0.05)
        s2_label = Text("Slave B", color=RED_E).scale(0.35).next_to(slave2, RIGHT, buff=0.05)

        board = checkerboard().scale(1.0).to_edge(LEFT, buff=1.2).shift(0.5*DOWN)
        tcp = Dot(color=WHITE).move_to(board.get_center()+0.8*DOWN+0.9*RIGHT)
        tcp_label = Text("TCP").scale(0.35).next_to(tcp, DOWN, buff=0.05)
        grasp = Arrow(tcp.get_center(), board.get_center(), buff=0, stroke_width=3, color=WHITE)

        self.play(LaggedStart(
            FadeIn(base, shift=UP),
            FadeIn(j1, shift=UP),
            FadeIn(rig, shift=UP),
            FadeIn(master, shift=UP),
            FadeIn(slave1, shift=UP),
            FadeIn(slave2, shift=UP),
            FadeIn(master_label),
            FadeIn(s1_label),
            FadeIn(s2_label),
            lag_ratio=0.1
        ))

        self.play(FadeIn(board, shift=RIGHT), FadeIn(tcp), FadeIn(tcp_label), GrowArrow(grasp))

        board_frame = coordinate_frame(scale=0.5).move_to(board.get_center())
        self.play(FadeIn(board_frame))

        cam_frames = VGroup()
        for cam in [master, slave1, slave2]:
            frame = coordinate_frame(scale=0.3).move_to(cam.get_center() + 0.5*DOWN)
            cam_frames.add(frame)
            self.play(FadeIn(frame), run_time=0.5)

        self.wait(0.5)

        positions = [
            board.get_center() + 0.8*UP + 0.5*LEFT,
            board.get_center() + 0.6*DOWN + 0.7*RIGHT,
            board.get_center() + 0.5*UP + 0.6*RIGHT,
        ]

        for pos in positions:
            new_tcp_pos = pos + 0.8*DOWN + 0.9*RIGHT
            self.play(
                board.animate.move_to(pos),
                board_frame.animate.move_to(pos),
                tcp.animate.move_to(new_tcp_pos),
                tcp_label.animate.next_to(Dot(new_tcp_pos), DOWN, buff=0.05),
                grasp.animate.put_start_and_end_on(new_tcp_pos, pos),
                run_time=1.2
            )
            self.wait(0.3)

        # Show rays / detections
        def rays_to_board(cam, col):
            return VGroup(
                Arrow(cam.get_center(), board.get_center()+0.25*UP, buff=0.1, color=col, stroke_width=2),
                Arrow(cam.get_center(), board.get_center()+0.25*DOWN, buff=0.1, color=col, stroke_width=2),
                Arrow(cam.get_center(), board.get_center()+0.25*RIGHT, buff=0.1, color=col, stroke_width=2)
            )

        r_master = rays_to_board(master, BLUE_E)
        r_s1 = rays_to_board(slave1, GREEN_E)
        r_s2 = rays_to_board(slave2, RED_E)
        self.play(*[GrowArrow(a) for a in r_master], run_time=1.0)
        self.play(*[GrowArrow(a) for a in r_s1], run_time=1.0)
        self.play(*[GrowArrow(a) for a in r_s2], run_time=1.0)

        # Show solved relative transforms
        link_s1 = DashedLine(master.get_center(), slave1.get_center(), color=GREEN_E)
        link_s2 = DashedLine(master.get_center(), slave2.get_center(), color=RED_E)
        lbl_s1 = Text("Solve  T(master->A)", color=GREEN_E).scale(0.35).next_to(link_s1, DOWN, buff=0.05)
        lbl_s2 = Text("Solve  T(master->B)", color=RED_E).scale(0.35).next_to(link_s2, DOWN, buff=0.05)

        self.play(ShowCreation(link_s1), FadeIn(lbl_s1, shift=DOWN))
        self.play(ShowCreation(link_s2), FadeIn(lbl_s2, shift=DOWN))

        # Caption
        cap = VGroup(
            Text("Robot moves marker; Bundle Adjustment solves transforms;"),
            Text("get camera-to-camera extrinsics.")
        ).arrange(DOWN, buff=0.15)
        cap.scale(0.6).to_edge(DOWN)
        self.play(FadeIn(cap, shift=UP))
        self.wait(1.2)

# ---------- Scene 2: Phase 2 (Axis identification by rotation) ----------

class Phase2Scene(Scene):
    def construct(self):
        title = Tex(r"\textbf{Phase 2: Pole Axis Identification (rotate the rig)}").to_edge(UP)
        self.play(FadeIn(title, shift=DOWN))

        base = robot_base().to_edge(DOWN, buff=0.3)
        j1 = j1_axis().next_to(base[0], UP, buff=0.1)

        rig = rig_mount()
        rig.move_to(j1.get_top() + 0.3*UP, aligned_edge=RIGHT)

        board = checkerboard().scale(1.0).to_edge(LEFT, buff=1.2).shift(0.5*DOWN)

        # Prepare axis visualization (but don't show yet)
        p = rig[1].get_center()
        axis_line = Arrow(p - 1.5*UP, p + 1.5*UP, color=YELLOW, buff=0, stroke_width=4)
        p_dot = Dot(point=p, color=YELLOW, radius=0.06)
        u_lbl = Text("u (axis dir)", color=YELLOW).scale(0.35).next_to(axis_line.get_top(), RIGHT, buff=0.1)
        p_lbl = Text("p (axis point)", color=YELLOW).scale(0.35).next_to(p_dot, RIGHT, buff=0.1)

        # Show camera moving on a circle around the axis (projected)
        radius = 0.8
        radius = 0.8
        a_radius = 0.8
        b_radius = 0.4

        def ellipse_point(t):
            return p + np.array([a_radius * np.cos(t), 0, b_radius * np.sin(t)])

        # Position camera at the starting point of the ellipse (t=0)
        master = camera_icon(BLUE_E).move_to(ellipse_point(0))

        self.play(FadeIn(base), FadeIn(j1), FadeIn(rig), FadeIn(master))
        self.play(FadeIn(board, shift=RIGHT))

        ellipse_dots = VGroup()
        for t in np.linspace(0, TAU, 80):
            if int(t*10) % 2 == 0:
                pt = ellipse_point(t)
                ellipse_dots.add(Dot(pt, radius=0.007, color=GREY_B))

        self.play(FadeIn(ellipse_dots))
        theta = ValueTracker(0)

        master.add_updater(lambda m: m.move_to(ellipse_point(theta.get_value())))

        def observation_rays():
            return VGroup(
                Arrow(master.get_center(), board.get_center()+0.3*UP, buff=0.1, color=BLUE_E, stroke_width=2),
                Arrow(master.get_center(), board.get_center(), buff=0.1, color=BLUE_E, stroke_width=2),
                Arrow(master.get_center(), board.get_center()+0.3*DOWN, buff=0.1, color=BLUE_E, stroke_width=2)
            )

        rays = always_redraw(observation_rays)
        self.add(rays)

        self.play(theta.animate.set_value(TAU), run_time=4, rate_func=linear)
        master.clear_updaters()
        self.remove(rays)

        # Now show the fitted axis after rotation completes
        self.play(GrowArrow(axis_line), FadeIn(p_dot), FadeIn(u_lbl), FadeIn(p_lbl))

        # Draw "fit" visualization
        fit_lbl = VGroup(
            Text("Fit axis direction u and point p"),
            Text("from circular camera motion")
        ).arrange(DOWN, buff=0.1).scale(0.5)
        fit_lbl.to_edge(DOWN)
        self.play(FadeIn(fit_lbl, shift=UP))
        self.wait(1.0)

# ---------- Scene 3: Phase 3 (Global BA over robot + pole + cameras) ----------

class Phase3Scene(Scene):
    def construct(self):
        title = VGroup(
            Tex(r"\textbf{Phase 3: Global Optimization}"),
            Text("Robot J1 <-> Pole <-> Cameras")
        ).arrange(DOWN, buff=0.1).to_edge(UP)
        self.play(FadeIn(title, shift=DOWN))

        base = robot_base().to_edge(DOWN, buff=0.3)
        j1 = j1_axis().next_to(base[0], UP, buff=0.1)

        rig = rig_mount()
        rig.move_to(j1.get_top() + 0.3*UP, aligned_edge=RIGHT)

        rig_top = rig[1].get_top()
        master = camera_icon(BLUE_E).move_to(rig_top + 0.3*DOWN + 0.2*LEFT)
        slave1 = camera_icon(GREEN_E).move_to(rig_top + 0.5*UP + 0.5*LEFT)
        slave2 = camera_icon(RED_E).move_to(rig_top + 0.5*UP + 0.1*RIGHT)

        board = checkerboard().scale(1.0).to_edge(LEFT, buff=1.2).shift(0.5*DOWN)

        self.play(
            FadeIn(base, shift=UP), FadeIn(j1, shift=UP), FadeIn(rig, shift=UP),
            FadeIn(master, shift=UP), FadeIn(slave1, shift=UP), FadeIn(slave2, shift=UP)
        )
        self.play(FadeIn(board, shift=RIGHT))

        tcp_dot = Dot(color=WHITE, radius=0.05).move_to(board.get_center() + 0.3*DOWN)
        tcp_label = Text("TCP", color=WHITE).scale(0.3).next_to(tcp_dot, DOWN, buff=0.05)

        self.play(FadeIn(tcp_dot), FadeIn(tcp_label))

        def rays(cam, col):
            return VGroup(
                Arrow(cam.get_center(), board.get_center()+0.3*UP, buff=0.1, color=col, stroke_width=2),
                Arrow(cam.get_center(), board.get_center(), buff=0.1, color=col, stroke_width=2),
                Arrow(cam.get_center(), board.get_center()+0.3*DOWN, buff=0.1, color=col, stroke_width=2)
            )

        rays_master = always_redraw(lambda: rays(master, BLUE_E))

        self.add(rays_master)

        board_group = VGroup(board, tcp_dot, tcp_label)

        positions = [
            board.get_center() + 0.5*RIGHT + 0.3*UP,
            board.get_center() + 0.8*RIGHT + 0.5*DOWN,
            board.get_center() + 0.3*LEFT + 0.6*UP,
            board.get_center()
        ]

        for pos in positions:
            self.play(
                board_group.animate.move_to(pos),
                run_time=1.2,
                rate_func=smooth
            )

        self.remove(rays_master)

        pole_joint = rig[2].get_center()
        j1_point = j1.get_center()

        transform_arrow = Arrow(j1_point, pole_joint, color=YELLOW, buff=0.1, stroke_width=6)
        transform_label = VGroup(
            Text("Calibrated:", color=YELLOW),
            Text("T(J1 -> Pole Joint)", color=YELLOW)
        ).arrange(DOWN, buff=0.05).scale(0.4)
        transform_label.next_to(transform_arrow, RIGHT, buff=0.2)

        self.play(GrowArrow(transform_arrow), FadeIn(transform_label))

        result_text = VGroup(
            Text("All transformations optimized:"),
            Text("Robot <-> Pole <-> Cameras")
        ).arrange(DOWN, buff=0.1).scale(0.45)
        result_text.to_edge(DOWN, buff=0.5)

        self.play(FadeIn(result_text, shift=UP))
        self.wait(2.0)
# ---------- Master scene stitching quick cuts ----------

class MasterScene(Scene):
    def construct(self):
        cover = Tex(r"\textbf{Rotating J1 Camera Pole: 3-Phase Calibration}").scale(0.9)
        subtitle = Tex(r"Phase 1: Cam-Cam \quad Phase 2: Axis \quad Phase 3: Global BA").scale(0.6).next_to(cover, DOWN)
        self.play(FadeIn(cover, shift=DOWN), FadeIn(subtitle, shift=UP))
        self.wait(1.5)
        self.play(*[FadeOut(m) for m in self.mobjects])

        Phase1Scene.construct(self)
        self.play(*[FadeOut(m) for m in self.mobjects])

        Phase2Scene.construct(self)
        self.play(*[FadeOut(m) for m in self.mobjects])

        Phase3Scene.construct(self)
        self.play(*[FadeOut(m) for m in self.mobjects])

        out = Tex(r"\textbf{Done!} \textit{Accurate, observable, and robust.}").scale(0.9)
        self.play(FadeIn(out, shift=UP))
        self.wait(1.5)
