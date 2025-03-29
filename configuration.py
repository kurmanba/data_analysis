from dataclasses import dataclass
from typing import Dict


@dataclass
class DirBoundary:
    st: int
    end: int
    tr1: int
    tr2: int
    accept: int


@dataclass
class DirectoryConfig:
    boundaries: Dict[str, DirBoundary]


@dataclass
class OpticsConfig:
    d: float  # in meters
    lambda_: float  # in nanometers
    I_ref: float  # dimensionless


@dataclass
class MaterialConfig:
    r_c: float  # in kg/m^3
    r_eg: float  # in kg/m^3
    eta: float  # in Pa·s
    diameter: float


@dataclass
class ElectricConfig:
    k_b: float  # in J/K
    T: float  # in K


@dataclass
class SetupConfig:
    time_multiplier: int
    ch1_multiplier: float
    ch2_multiplier: int
    rotation: int
    sigma: int
    cut: int


@dataclass
class RegConfig:
    lambda_reg: float
    n_tau: int


@dataclass
class FitConfig:
    gradient_threshold: float
    gradient_award: int
    sgf_window: int
    time_threshold: int
    dn_stability_index: int
    exp_smoothing_factor: float
    d_fall_guess: float
    gaussian_factor: float
    standard_time: int
    standard_sampling: float


@dataclass
class FieldsConfig:
    # voltages: list
    flows: list
    pulse_width: list
    concentrations: list


@dataclass
class BaseDirsConfig:
    database: str
    logs: str
    digested: str
    figures: str
    raw_folder: str
    raw_folder_damage: str


@dataclass
class ExperimentConfig:
    optics: OpticsConfig
    material: MaterialConfig
    electric: ElectricConfig
    setup: SetupConfig
    reg: RegConfig
    fit: FitConfig
    potentials: FieldsConfig
    base_dirs: BaseDirsConfig
    directories: DirectoryConfig  # added field for directory boundaries


def get_experiment_config() -> ExperimentConfig:
    return ExperimentConfig(
            optics=OpticsConfig(
                    d=2.2e-3,
                    lambda_=632.8e-9,
                    I_ref=5_000.0,
            ),
            material=MaterialConfig(
                    r_c=1650,
                    r_eg=1113,
                    eta=0.0161,
                    diameter=100e-9,
            ),
            electric=ElectricConfig(
                    k_b=1.380649e-23,
                    T=298.5,
            ),
            setup=SetupConfig(
                    time_multiplier=1000,
                    ch1_multiplier=4.5,
                    ch2_multiplier=1000,
                    rotation=-1,
                    sigma=7,
                    cut=17000
            ),
            reg=RegConfig(
                    lambda_reg=0.05,
                    n_tau=500,
            ),
            fit=FitConfig(
                    gradient_threshold=0.1,
                    gradient_award=5,
                    sgf_window=101,
                    time_threshold=2,
                    dn_stability_index=500,
                    exp_smoothing_factor=4,
                    d_fall_guess=0.0025,
                    gaussian_factor=5,
                    standard_time=250,
                    standard_sampling=0.03200021,
            ),
            potentials=FieldsConfig(
                    pulse_width=[300, 200, 150, 100],
                    concentrations=["00078", "00156", "00312", "00625"],
                    # voltages=[1, 2, 3, 4, 5, 6],
                    flows=[0],
            ),
            base_dirs=BaseDirsConfig(
                    database="/Users/alisher/IdeaProjects/TEB_REMAKE/databases",
                    logs="/Users/alisher/IdeaProjects/TEB_REMAKE/logs",
                    digested="/Users/alisher/IdeaProjects/TEB_REMAKE/digested",
                    figures="/Users/alisher/IdeaProjects/TEB_REMAKE/figures",
                    raw_folder='/Users/alisher/IdeaProjects/TEB_REMAKE/raw_pulses',
                    raw_folder_damage="/Users/alisher/IdeaProjects/TEB_REMAKE/Experimtents/Damage_experiment",
            ),
            directories=DirectoryConfig(
                    boundaries={
                            # 00078/0/300

                            "00078/0/300/TEK00001": DirBoundary(st=None, end=None, tr1=None, tr2=None, accept=None),
                            "00078/0/300/TEK00000": DirBoundary(st=None, end=None, tr1=None, tr2=None, accept=None),
                            "00078/0/300/TEK00014": DirBoundary(st=None, end=None, tr1=None, tr2=None, accept=None),
                            "00078/0/300/TEK00002": DirBoundary(st=None, end=None, tr1=None, tr2=None, accept=None),
                            "00078/0/300/TEK00003": DirBoundary(st=None, end=None, tr1=None, tr2=None, accept=None),
                            "00078/0/300/TEK00007": DirBoundary(st=None, end=None, tr1=None, tr2=None, accept=None),
                            "00078/0/300/TEK00013": DirBoundary(st=None, end=None, tr1=None, tr2=None, accept=None),
                            "00078/0/300/TEK00012": DirBoundary(st=None, end=None, tr1=None, tr2=None, accept=None),
                            "00078/0/300/TEK00006": DirBoundary(st=None, end=None, tr1=None, tr2=None, accept=None),
                            "00078/0/300/TEK00004": DirBoundary(st=None, end=None, tr1=None, tr2=None, accept=None),
                            "00078/0/300/TEK00005": DirBoundary(st=None, end=None, tr1=None, tr2=None, accept=None),
                            "00078/0/300/TEK00011": DirBoundary(st=None, end=None, tr1=None, tr2=None, accept=None),
                            "00078/0/300/TEK00008": DirBoundary(st=None, end=None, tr1=None, tr2=None, accept=None),
                            "00078/0/300/TEK00009": DirBoundary(st=None, end=None, tr1=None, tr2=None, accept=None),

                            # 00078/0/200

                            "00078/0/200/TEK00001": DirBoundary(st=None, end=None, tr1=None, tr2=None, accept=None),
                            "00078/0/200/TEK00014": DirBoundary(st=None, end=None, tr1=None, tr2=None, accept=None),
                            "00078/0/200/TEK00002": DirBoundary(st=None, end=None, tr1=None, tr2=None, accept=None),
                            "00078/0/200/TEK00007": DirBoundary(st=None, end=None, tr1=None, tr2=None, accept=None),
                            "00078/0/200/TEK00013": DirBoundary(st=None, end=None, tr1=None, tr2=None, accept=None),
                            "00078/0/200/TEK00012": DirBoundary(st=None, end=None, tr1=None, tr2=None, accept=None),
                            "00078/0/200/TEK00006": DirBoundary(st=None, end=None, tr1=None, tr2=None, accept=None),
                            "00078/0/200/TEK00010": DirBoundary(st=None, end=None, tr1=None, tr2=None, accept=None),
                            "00078/0/200/TEK00005": DirBoundary(st=None, end=None, tr1=None, tr2=None, accept=None),
                            "00078/0/200/TEK00011": DirBoundary(st=None, end=None, tr1=None, tr2=None, accept=None),
                            "00078/0/200/TEK00008": DirBoundary(st=None, end=None, tr1=None, tr2=None, accept=None),
                            "00078/0/200/TEK00009": DirBoundary(st=None, end=None, tr1=None, tr2=None, accept=None),

                            # 00078/0/150

                            "00078/0/150/TEK00001": DirBoundary(st=None, end=None, tr1=None, tr2=None, accept=None),
                            "00078/0/150/TEK00000": DirBoundary(st=None, end=None, tr1=None, tr2=None, accept=None),
                            "00078/0/150/TEK00002": DirBoundary(st=None, end=None, tr1=None, tr2=None, accept=None),
                            "00078/0/150/TEK00003": DirBoundary(st=None, end=None, tr1=None, tr2=None, accept=None),
                            "00078/0/150/TEK00006": DirBoundary(st=None, end=None, tr1=None, tr2=None, accept=None),
                            "00078/0/150/TEK00004": DirBoundary(st=None, end=None, tr1=None, tr2=None, accept=None),
                            "00078/0/150/TEK00005": DirBoundary(st=None, end=None, tr1=None, tr2=None, accept=None),

                            # 00078/0/100

                            "00078/0/100/TEK00001": DirBoundary(st=None, end=None, tr1=None, tr2=None, accept=None),
                            "00078/0/100/TEK00000": DirBoundary(st=None, end=None, tr1=None, tr2=None, accept=None),
                            "00078/0/100/TEK00002": DirBoundary(st=None, end=None, tr1=None, tr2=None, accept=None),
                            "00078/0/100/TEK00003": DirBoundary(st=None, end=None, tr1=None, tr2=None, accept=None),
                            "00078/0/100/TEK00004": DirBoundary(st=None, end=None, tr1=None, tr2=None, accept=None),
                            "00078/0/100/TEK00005": DirBoundary(st=None, end=None, tr1=None, tr2=None, accept=None),

                            # 00156/0/300

                            "00156/0/300/TEK00001": DirBoundary(st=538, end=9670, tr1=None, tr2=None, accept=None),
                            "00156/0/300/TEK00000": DirBoundary(st=538, end=9520, tr1=None, tr2=None, accept=None),
                            "00156/0/300/TEK00002": DirBoundary(st=538, end=9750, tr1=None, tr2=None, accept=None),
                            "00156/0/300/TEK00003": DirBoundary(st=538, end=9750, tr1=None, tr2=None, accept=None),
                            "00156/0/300/TEK00007": DirBoundary(st=538, end=9650, tr1=None, tr2=None, accept=None),
                            "00156/0/300/TEK00006": DirBoundary(st=538, end=9750, tr1=None, tr2=None, accept=None),
                            "00156/0/300/TEK00010": DirBoundary(st=538, end=9670, tr1=None, tr2=None, accept=None),
                            "00156/0/300/TEK00004": DirBoundary(st=538, end=9750, tr1=None, tr2=None, accept=None),
                            "00156/0/300/TEK00008": DirBoundary(st=538, end=9750, tr1=None, tr2=None, accept=None),
                            "00156/0/300/TEK00009": DirBoundary(st=538, end=9670, tr1=None, tr2=None, accept=None),

                            # 00156/0/200

                            "00156/0/200/TEK00001": DirBoundary(st=535, end=6520, tr1=None, tr2=None, accept=None),
                            "00156/0/200/TEK00002": DirBoundary(st=535, end=6200, tr1=None, tr2=None, accept=None),
                            "00156/0/200/TEK00003": DirBoundary(st=535, end=6450, tr1=None, tr2=None, accept=None),
                            "00156/0/200/TEK00006": DirBoundary(st=535, end=6450, tr1=None, tr2=None, accept=None),
                            "00156/0/200/TEK00010": DirBoundary(st=535, end=6200, tr1=None, tr2=None, accept=None),
                            "00156/0/200/TEK00004": DirBoundary(st=535, end=6450, tr1=None, tr2=None, accept=None),
                            "00156/0/200/TEK00005": DirBoundary(st=535, end=6450, tr1=None, tr2=None, accept=None),
                            # 00156/0/150
                            "00156/0/150/TEK00001": DirBoundary(st=537, end=4700, tr1=None, tr2=None, accept=None),
                            "00156/0/150/TEK00000": DirBoundary(st=537, end=4780, tr1=None, tr2=None, accept=None),
                            "00156/0/150/TEK00002": DirBoundary(st=537, end=4700, tr1=None, tr2=None, accept=None),
                            "00156/0/150/TEK00003": DirBoundary(st=537, end=4700, tr1=None, tr2=None, accept=None),
                            "00156/0/150/TEK00007": DirBoundary(st=537, end=4700, tr1=None, tr2=None, accept=None),
                            "00156/0/150/TEK00006": DirBoundary(st=537, end=4700, tr1=None, tr2=None, accept=None),
                            "00156/0/150/TEK00004": DirBoundary(st=537, end=4750, tr1=None, tr2=None, accept=None),
                            "00156/0/150/TEK00005": DirBoundary(st=537, end=4700, tr1=None, tr2=None, accept=None),
                            # 00156/0/100
                            "00156/0/100/TEK00001": DirBoundary(st=520, end=3060, tr1=None, tr2=None, accept=None),
                            "00156/0/100/TEK00000": DirBoundary(st=520, end=3120, tr1=None, tr2=None, accept=None),
                            "00156/0/100/TEK00002": DirBoundary(st=520, end=3000, tr1=None, tr2=None, accept=None),
                            "00156/0/100/TEK00003": DirBoundary(st=520, end=3000, tr1=None, tr2=None, accept=None),
                            "00156/0/100/TEK00006": DirBoundary(st=520, end=3000, tr1=None, tr2=None, accept=None),
                            "00156/0/100/TEK00004": DirBoundary(st=520, end=3000, tr1=None, tr2=None, accept=None),
                            "00156/0/100/TEK00005": DirBoundary(st=520, end=3000, tr1=None, tr2=None, accept=None),
                            # 00312/0/300
                            "00312/0/300/TEK00001": DirBoundary(st=520, end=9600, tr1=None, tr2=None, accept=None),
                            "00312/0/300/TEK00000": DirBoundary(st=520, end=9300, tr1=None, tr2=None, accept=None),
                            "00312/0/300/TEK00002": DirBoundary(st=520, end=9600, tr1=None, tr2=None, accept=None),
                            "00312/0/300/TEK00003": DirBoundary(st=520, end=9600, tr1=None, tr2=None, accept=None),
                            "00312/0/300/TEK00007": DirBoundary(st=520, end=9600, tr1=None, tr2=None, accept=None),
                            "00312/0/300/TEK00006": DirBoundary(st=520, end=9600, tr1=None, tr2=None, accept=None),
                            "00312/0/300/TEK00004": DirBoundary(st=520, end=9600, tr1=None, tr2=None, accept=None),
                            "00312/0/300/TEK00005": DirBoundary(st=520, end=9600, tr1=None, tr2=None, accept=None),
                            "00312/0/300/TEK00008": DirBoundary(st=520, end=9600, tr1=None, tr2=None, accept=None),
                            # 00312/0/200
                            "00312/0/200/TEK00001": DirBoundary(st=525, end=6300, tr1=None, tr2=None, accept=None),
                            "00312/0/200/TEK00000": DirBoundary(st=525, end=5750, tr1=None, tr2=None, accept=None),
                            "00312/0/200/TEK00002": DirBoundary(st=525, end=6300, tr1=None, tr2=None, accept=None),
                            "00312/0/200/TEK00003": DirBoundary(st=525, end=6300, tr1=None, tr2=None, accept=None),
                            "00312/0/200/TEK00006": DirBoundary(st=525, end=6300, tr1=None, tr2=None, accept=None),
                            "00312/0/200/TEK00004": DirBoundary(st=525, end=6300, tr1=None, tr2=None, accept=None),
                            "00312/0/200/TEK00005": DirBoundary(st=525, end=6300, tr1=None, tr2=None, accept=None),
                            "00312/0/200/TEK00008": DirBoundary(st=525, end=6300, tr1=None, tr2=None, accept=None),
                            "00312/0/200/TEK00009": DirBoundary(st=525, end=6300, tr1=None, tr2=None, accept=None),
                            # 00312/0/150
                            "00312/0/150/TEK00001": DirBoundary(st=525, end=4750, tr1=None, tr2=None, accept=None),
                            "00312/0/150/TEK00000": DirBoundary(st=525, end=4750, tr1=None, tr2=None, accept=None),
                            "00312/0/150/TEK00002": DirBoundary(st=525, end=4750, tr1=None, tr2=None, accept=None),
                            "00312/0/150/TEK00003": DirBoundary(st=525, end=4750, tr1=None, tr2=None, accept=None),
                            "00312/0/150/TEK00007": DirBoundary(st=525, end=4750, tr1=None, tr2=None, accept=None),
                            "00312/0/150/TEK00006": DirBoundary(st=525, end=4750, tr1=None, tr2=None, accept=None),
                            "00312/0/150/TEK00004": DirBoundary(st=525, end=4750, tr1=None, tr2=None, accept=None),
                            "00312/0/150/TEK00005": DirBoundary(st=525, end=4750, tr1=None, tr2=None, accept=None),
                            # 00312/0/100
                            "00312/0/100/TEK00001": DirBoundary(st=515, end=3000, tr1=None, tr2=None, accept=None),
                            "00312/0/100/TEK00000": DirBoundary(st=515, end=3000, tr1=None, tr2=None, accept=None),
                            "00312/0/100/TEK00002": DirBoundary(st=515, end=3000, tr1=None, tr2=None, accept=None),
                            "00312/0/100/TEK00003": DirBoundary(st=515, end=3000, tr1=None, tr2=None, accept=None),
                            "00312/0/100/TEK00007": DirBoundary(st=515, end=3000, tr1=None, tr2=None, accept=None),
                            "00312/0/100/TEK00006": DirBoundary(st=515, end=3000, tr1=None, tr2=None, accept=None),
                            "00312/0/100/TEK00004": DirBoundary(st=515, end=3000, tr1=None, tr2=None, accept=None),
                            "00312/0/100/TEK00005": DirBoundary(st=515, end=3000, tr1=None, tr2=None, accept=None),
                            # 00625/0/300
                            "00625/0/300/TEK00001": DirBoundary(st=543, end=9870, tr1=None, tr2=None, accept=1),
                            "00625/0/300/TEK00000": DirBoundary(st=543, end=9870, tr1=None, tr2=None, accept=0),
                            "00625/0/300/TEK00002": DirBoundary(st=543, end=9870, tr1=None, tr2=None, accept=1),
                            "00625/0/300/TEK00003": DirBoundary(st=543, end=9870, tr1=None, tr2=None, accept=1),
                            "00625/0/300/TEK00004": DirBoundary(st=543, end=9870, tr1=None, tr2=None, accept=1),
                            "00625/0/300/TEK00005": DirBoundary(st=543, end=9870, tr1=None, tr2=None, accept=1),
                            # 00625/0/200
                            "00625/0/200/TEK00001": DirBoundary(st=543, end=6700, tr1=None, tr2=None, accept=0),
                            "00625/0/200/TEK00000": DirBoundary(st=543, end=6720, tr1=None, tr2=None, accept=0),
                            "00625/0/200/TEK00002": DirBoundary(st=543, end=6700, tr1=None, tr2=None, accept=1),
                            "00625/0/200/TEK00003": DirBoundary(st=543, end=6690, tr1=None, tr2=None, accept=1),
                            "00625/0/200/TEK00010": DirBoundary(st=543, end=6720, tr1=None, tr2=None, accept=1),
                            "00625/0/200/TEK00004": DirBoundary(st=543, end=6683, tr1=None, tr2=None, accept=1),
                            "00625/0/200/TEK00005": DirBoundary(st=543, end=6660, tr1=None, tr2=None, accept=1),
                            "00625/0/200/TEK00011": DirBoundary(st=543, end=6770, tr1=None, tr2=None, accept=0),
                            "00625/0/200/TEK00009": DirBoundary(st=543, end=6710, tr1=None, tr2=None, accept=1),
                            # 00625/0/150
                            "00625/0/150/TEK00001": DirBoundary(st=543, end=4880, tr1=None, tr2=None, accept=None),
                            "00625/0/150/TEK00000": DirBoundary(st=543, end=5025, tr1=None, tr2=None, accept=None),
                            "00625/0/150/TEK00002": DirBoundary(st=543, end=4880, tr1=None, tr2=None, accept=None),
                            "00625/0/150/TEK00003": DirBoundary(st=543, end=4880, tr1=None, tr2=None, accept=None),
                            "00625/0/150/TEK00006": DirBoundary(st=543, end=4820, tr1=None, tr2=None, accept=None),
                            "00625/0/150/TEK00010": DirBoundary(st=543, end=4880, tr1=None, tr2=None, accept=None),
                            "00625/0/150/TEK00004": DirBoundary(st=543, end=4880, tr1=None, tr2=None, accept=None),
                            "00625/0/150/TEK00005": DirBoundary(st=543, end=4900, tr1=None, tr2=None, accept=None),
                            "00625/0/150/TEK00011": DirBoundary(st=543, end=4671, tr1=None, tr2=None, accept=None),
                            "00625/0/150/TEK00009": DirBoundary(st=543, end=4930, tr1=None, tr2=None, accept=None),
                            # 00625/0/100
                            "00625/0/100/TEK00001": DirBoundary(st=543, end=3300, tr1=None, tr2=None, accept=None),
                            "00625/0/100/TEK00000": DirBoundary(st=543, end=3370, tr1=None, tr2=None, accept=None),
                            "00625/0/100/TEK00002": DirBoundary(st=543, end=3300, tr1=None, tr2=None, accept=None),
                            "00625/0/100/TEK00003": DirBoundary(st=543, end=3300, tr1=None, tr2=None, accept=None),
                            "00625/0/100/TEK00007": DirBoundary(st=543, end=3300, tr1=None, tr2=None, accept=None),
                            "00625/0/100/TEK00006": DirBoundary(st=543, end=3300, tr1=None, tr2=None, accept=None),
                            "00625/0/100/TEK00004": DirBoundary(st=543, end=3300, tr1=None, tr2=None, accept=None),
                            "00625/0/100/TEK00005": DirBoundary(st=543, end=3300, tr1=None, tr2=None, accept=None),
                    }
            ),
    )


if __name__ == "__main__":
    pass
