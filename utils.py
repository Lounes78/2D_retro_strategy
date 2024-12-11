def update_map(file_path, grid, new_letter, position, already_occupied, distance=2):
    if grid is None:
        with open(file_path, "r") as file:
            grid = file.readlines()

    grid = [line.strip() for line in grid]

    parsed_grid = [row.split("][") for row in grid]
    parsed_grid = [[cell.strip("[]") for cell in row] for row in parsed_grid]

    if new_letter == '*':   
        for r in range(len(parsed_grid)):
            for c in range(len(parsed_grid[0])):
                parsed_grid[r][c] = '1:G'
    else:
        max_row = len(parsed_grid)
        max_col = len(parsed_grid[0]) if max_row > 0 else 0

        row, col = position
        for r in range(max(0, row - distance), min(max_row, row + distance + 1)):
            for c in range(max(0, col - distance), min(max_col, col + distance + 1)):
                if (r, c) not in already_occupied:
                    if (r, c) == position:
                        parsed_grid[r][c] = "2:K"
                    else:
                        parsed_grid[r][c] = f"1:{new_letter}"

    modified_grid = [
        "".join(f"[{cell}]" for cell in row) for row in parsed_grid
    ]

    # with open(file_path, "w") as file:
    #     file.write("\n".join(modified_grid))
    #     file.flush()  # Ensure data is written to disk
    #     os.fsync(file.fileno())  

    return modified_grid