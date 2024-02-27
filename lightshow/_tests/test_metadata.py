import json
from pathlib import Path

from lightshow.parameters.feff import FEFFParameters


def test_multiplicipty_writing(database_from_file, tmp_path):
    target = Path(tmp_path) / Path("multi") / Path("destination")
    target.mkdir(exist_ok=True, parents=True)
    R = 10.0
    feff_parameters = FEFFParameters(
        cards={
            "S02": "0",
            "COREHOLE": "RPA",
            "CONTROL": "1 1 1 1 1 1",
            "XANES": "4 0.04 0.1",
            "SCF": "7.0 0 100 0.2 3",
            "FMS": "9.0 0",
            "EXCHANGE": "0 0.0 0.0 2",
            "RPATH": "-1",
        },
        edge="K",
        radius=R - 1.0,
        spectrum="XANES",
        name="FEFF",
    )
    database_from_file.write(
        target,
        absorbing_atoms="all",
        options=[feff_parameters],
        write_unit_cells=True,
        pbar=False,
    )
    metadata_fn = target / Path("00000002") / Path("metadata.json")
    with open(metadata_fn) as f:
        d_metadata = json.load(f)
    assert "multiplicities" in d_metadata
    i_site, n_multi = 2, 4
    assert d_metadata[i_site] == n_multi
