
import gc

__all__ = ["hold", "clear", "set_canvas", "get_canvas"]

global collector
collector = []

global main_canvas
main_canvas = None


def hold( obj ):
    global collector
    collector.append(obj)

def clear():
  global collector
  collector = []
  gc.collect()

def set_canvas( canvas ):
    global main_canvas
    if main_canvas:
        main_canvas.Close()
        main_canvas.Delete()
    main_canvas = canvas

def get_canvas():
    global main_canvas
    return main_canvas

