"""Main entry point."""

import argparse
import gif_your_nifti.config as cfg
from gif_your_nifti import core, __version__
import warnings  # mainly for ignoring imageio warnings
warnings.filterwarnings("ignore")


def main():
    """Commandline interface."""
    parser = argparse.ArgumentParser()

    parser.add_argument(
        'filename',  metavar='path', nargs='+',
        help="Path to image. Multiple paths can be provided."
        )
    parser.add_argument(
        '--mode', type=str, required=False,
        metavar=cfg.mode, default=cfg.mode,
        help="Gif creation mode. Available options are: 'normal', \
        'pseudocolor', 'depth', 'rgb'"
        )
    parser.add_argument(
        '--fps', type=int, required=False,
        metavar=cfg.fps, default=cfg.fps,
        help="Frames per second."
        )
    parser.add_argument(
        '--size', type=float, required=False,
        metavar=cfg.size, default=cfg.size,
        help="Image resizing factor."
        )
    parser.add_argument(
        '--cmap', type=str, required=False,
        metavar=cfg.cmap, default=cfg.cmap,
        help="Color map. Used only in combination with 'pseudocolor' mode."
        )

    parser.add_argument(
        '--sliceCor', type=int, required=False,
        metavar=cfg.sliceCor, default=cfg.sliceCor,
        help="Slice index for Coronal view."
    )

    parser.add_argument(
        '--sliceSag', type=int, required=False,
        metavar=cfg.sliceSag, default=cfg.sliceSag,
        help="Slice index for Sagital view."
    )

    parser.add_argument(
        '--sliceAx', type=int, required=False,
        metavar=cfg.sliceAx, default=cfg.sliceAx,
        help="Slice index for Axial view."
    )

    parser.add_argument(
        '--slicesOrder', type=str, required=False,
        metavar=cfg.slicesOrder, default='csa',
        help="Order of the three columns cortical, sagital, axial."
                " Can be csa, cas, asc, acs, sac or sca."
    )

    parser.add_argument(
        '--out_filename', type=str, required=False,
        default=None,
        help="Output GIF filename with extension."
    )

    args = parser.parse_args()
    cfg.mode = (args.mode).lower()
    cfg.size = args.size
    cfg.fps = args.fps
    cfg.cmap = args.cmap

    cfg.slices = [args.sliceCor, args.sliceSag, args.sliceAx]
    cfg.slicesOrder = args.slicesOrder

    # Determine gif creation mode
    if cfg.mode in ['normal', 'pseudocolor', 'depth']:
        for f in args.filename:
            if cfg.mode == 'normal':
                core.write_gif_normal(f, cfg.size, cfg.fps,
                                      cfg.slices, cfg.slicesOrder,
                                      args.out_filename)
            elif cfg.mode == 'pseudocolor':
                core.write_gif_pseudocolor(f, cfg.size, cfg.fps, cfg.cmap,
                                           cfg.slices, cfg.slicesOrder,
                                           args.out_filename)
            elif cfg.mode == 'depth':
                core.write_gif_depth(f, cfg.size, cfg.fps, args.out_filename)

    elif cfg.mode == 'rgb':
        if len(args.filename) != 3:
            raise ValueError('RGB mode requires 3 input files.')
        else:
            core.write_gif_rgb(args.filename[0], args.filename[1],
                               args.filename[2], cfg.size, cfg.fps,
                               args.out_filename)
    else:
        raise ValueError("Unrecognized mode.")

    #print('Finished.')


if __name__ == "__main__":
    main()
