def grid_frame(frame, frame_rows=[0], frame_cols=[0], origin_row=0, origin_column=0, origin_sticky='snwe'):
    if origin_row is not None and origin_column is not None and origin_sticky is not None:
        frame.grid(row=origin_row, column=origin_column, sticky=origin_sticky)
    for row in frame_rows:
        frame.rowconfigure(row, weight=1)
    for col in frame_cols:
        frame.columnconfigure(col, weight=1)
