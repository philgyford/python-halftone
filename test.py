import halftone


h = halftone.Halftone("/Users/phil/Desktop/_testpics/cmyk.jpg")
h.make(
    style="color",
    save_channels=True,
    save_channels_style="color",
    save_channels_format="png",
    percentage=100,
    antialias=True,
    output_quality=80,
    output_format="png"

)
