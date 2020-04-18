def grid_frame(frame, frame_rows=[0], frame_cols=[0], parent_row=0, parent_column=0, frame_sticky='snwe', is_root=False):
    if is_root:
        frame.grid()
    else:
        frame.grid(row=parent_row, column=parent_column, sticky=frame_sticky)
    for row in frame_rows:
        frame.rowconfigure(row, weight=1)
    for col in frame_cols:
        frame.columnconfigure(col, weight=1)
