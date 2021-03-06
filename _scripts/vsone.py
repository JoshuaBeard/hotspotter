import sys
import hotspotter.params as params
import hotspotter.load_data2 as ld2
import hotspotter.match_chips2 as mc2
import hotspotter.draw_func2 as df2
import hotspotter.params
import hotspotter.helpers as helpers
import pyflann

def get_vsone_flann(data):
    vsone_flann = pyflann.FLANN()
    vsone_flann_params =  params.VSONE_FLANN_PARAMS
    ratio_thresh = params.__VSONE_RATIO_THRESH__
    checks = vsone_flann_params['checks']
    vsone_flann.build_index(data, **vsone_flann_params)
    return vsone_flann, checks

# Database descriptor + keypoints
def get_features(hs, cx):
    rchip    = hs.get_chip(cx)
    fx2_kp   = hs.feats.cx2_kpts[cx]
    fx2_desc = hs.feats.cx2_desc[cx]
    return cx, rchip, fx2_kp, fx2_desc

def get_vsone_data(query_feats, result_feats):
    ' Assigned matches (vsone)'
    qcx, rchip1, fx2_kp1, fx2_desc1 = query_feats
    cx, rchip2, fx2_kp2, fx2_desc2 = result_feats
    rchip_size2 = rchip2.size
    vsone_flann, checks = get_vsone_flann(fx2_desc1)
    fm, fs              = mc2.match_vsone(fx2_desc2, vsone_flann, checks)
    fm_V, fs_V          = mc2.spatially_verify(fx2_kp1, fx2_kp2, rchip_size2, fm, fs)
    score = fs.sum(); score_V = fs_V.sum()
    vsone_cx_assign = fm, fs, score
    vsone_cx_svout = fm_V, fs_V, score_V
    return vsone_cx_assign, vsone_cx_svout

def show_vsone_data(query_feats, result_feats, vsone_data, fignum=0, figtitle=''):
    vsone_cx_assign, vsone_cx_svout = vsone_data
    # Show vsone
    qcx, rchip1, fx2_kp1, fx2_desc1 = query_feats
    cx, rchip2, fx2_kp2, fx2_desc2 = result_feats
    fm, fs, score       = vsone_cx_assign
    fm_V, fs_V, score_V = vsone_cx_svout
    plot_kwargs = dict(all_kpts=False, fignum=fignum)
    df2.show_matches2(rchip1, rchip2, fx2_kp1, fx2_kp2, fm, fs,
                        plotnum=(1,2,1), title='vsone assign', **plot_kwargs)
    df2.show_matches2(rchip1, rchip2, fx2_kp1, fx2_kp2, fm_V, fs_V,
                        plotnum=(1,2,2), title='vsone verified', **plot_kwargs)
    df2.set_figtitle(figtitle)

# ------------------

def show_vsone_demo(hs, qcx, cx, fignum=0):
    print('[demo] vsone')
    print('qcx=%r, cx=%r' % (qcx, cx))
    # Query and Result features
    query_feats = get_features(hs, qcx)
    result_feats = get_features(hs, cx)
    query_uid = params.get_query_uid()
    vsone_data = get_vsone_data(query_feats, result_feats)
    figtitle = '%r v %r -- vsone' % (qcx, cx)
    show_vsone_data(query_feats, result_feats, vsone_data, fignum, figtitle)

# Assign + Verify
#params.__USE_CHIP_EXTENT__ = False
#vsone_data = get_vsone_data(cx)
#params.__USE_CHIP_EXTENT__ = True
#vsone_data2 = get_vsone_data(cx)
if __name__ == '__main__':
    import multiprocessing
    multiprocessing.freeze_support()
    db_dir = params.DEFAULT
    if not 'hs' in vars():
        hs = ld2.HotSpotter()
        hs.load_all(db_dir, matcher=False)
        qcx = helpers.get_arg_after('--qcx', type_=int, default=0)
        cx = helpers.get_arg_after('--cx', type_=int)
        if cx is None:
            cx_list = hs.get_other_cxs(qcx)
        else:
            cx_list = [cx]
        
    print('cx_list = %r ' % cx_list)
    for fignum, cx in enumerate(cx_list):
        show_vsone_demo(hs, qcx, cx, fignum=fignum)
    exec(df2.present())
'''
python vsone.py GZ --qcx 1046
'''
