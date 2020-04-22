

def grid_frame(
    frame,
    frame_rows=[0],
    frame_cols=[0],
    parent_row=0,
    parent_column=0,
    frame_sticky='snwe',
    is_root=False
):
    """Grid ``frame`` and configure ``frame_rows`` and ``frame_cols``.

    ``frame_rows``, ``frame_cols``:
        Lists of indexes of ``frame`` rows and cols respectively to configue.
        These rows and cols become stretchable.

    ``parent_row``, ``parent_col``, ``frame_sticky``:
        ``frame.grid`` arguments: ``row``, ``col``, ``sticky`` respectively.

    If ``is_root``, ``parent_col``, ``parent_row`` and ``frame_sticky``
    are ignored.
    """
    if is_root:
        frame.grid()
    else:
        frame.grid(row=parent_row, column=parent_column, sticky=frame_sticky)
    for row in frame_rows:
        frame.rowconfigure(row, weight=1)
    for col in frame_cols:
        frame.columnconfigure(col, weight=1)
