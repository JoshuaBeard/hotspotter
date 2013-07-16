def report_results(cx2_res, hs_tables):
    cx2_cid = hs_tables.cx2_cid
    cx2_nx  = hs_tables.cx2_nx
    cx2_top_truepos_rank  = np.zeros(len(cx2_cid)) - 100
    cx2_top_truepos_score = np.zeros(len(cx2_cid)) - 100
    cx2_top_trueneg_rank  = np.zeros(len(cx2_cid)) - 100
    cx2_top_trueneg_score = np.zeros(len(cx2_cid)) - 100
    cx2_top_score         = np.zeros(len(cx2_cid)) - 100
    for qcx, qcid in enumerate(cx2_cid):
        qnx = cx2_nx[qcx]
        res = cx2_res[qcx]
        # The score is the sum of the feature scores
        cx2_score = np.array([np.sum(fs) for fs in res.cx2_fs])
        top_cx = np.argsort(cx2_score)[::-1]
        top_score = cx2_score[top_cx]
        top_nx = cx2_nx[top_cx]
        # Remove query from true positives ranks
        _truepos_ranks, = np.where(top_nx == qnx)
        # Get TRUE POSTIIVE ranks
        truepos_ranks = _truepos_ranks[top_cx[_truepos_ranks] != qcx]
        # Get BEST True Positive and BEST True Negative
        if len(truepos_ranks) > 0:
            top_truepos_rank = truepos_ranks.min()
            bot_truepos_rank = truepos_ranks.max()
            true_neg_range   = np.arange(0, bot_truepos_rank+2)
            top_trueneg_rank = np.setdiff1d(true_neg_range, truepos_ranks).min()
            top_trupos_score = top_score[top_truepos_rank]
        else:
            top_trueneg_rank = 0
            top_truepos_rank = np.NAN
            top_trupos_score = np.NAN
        # Append stats to output
        cx2_top_truepos_rank[qcx]  = top_truepos_rank
        cx2_top_truepos_score[qcx] = top_trupos_score
        cx2_top_trueneg_rank[qcx]  = top_trueneg_rank
        cx2_top_trueneg_score[qcx] = top_score[top_trueneg_rank]
        cx2_top_score[qcx]         = top_score[0]
    # difference between the top score and the actual best score
    cx2_score_disp = cx2_top_score - cx2_top_true_score
    #
    # Easy to digest results
    num_chips = len(cx2_top_truepos_rank)
    num_with_gtruth = (1 - np.isnan(cx2_top_truepos_rank)).sum()
    num_rank_less5 = (cx2_top_truepos_rank < 5).sum()
    num_rank_less1 = (cx2_top_truepos_rank < 1).sum()
    
    # Display ranking results
    rankres_str = ('#TTP = top true positive #TTN = top true negative\n')
    rankres_header = '#CID, TTP RANK, TTN RANK, TTP SCORE, TTN SCORE, SCORE DISP, NAME\n'
    rankres_str += rankres_header
    todisp = np.vstack([cx2_cid,
                        cx2_top_truepos_rank,
                        cx2_top_trueneg_rank,
                        cx2_top_truepos_score,
                        cx2_top_trueneg_score,
                        cx2_score_disp, 
                        cx2_nx]).T
    for (cid, ttpr, ttnr, ttps, ttns, sdisp, nx) in todisp:
        rankres_str+=('%4d, %8.0f, %8.0f, %9.2f, %9.2f, %10.2f, %s\n' %\
              (cid, ttpr, ttnr, ttps, ttns, sdisp, nx2_name[nx]) )
    rankres_str += rankres_header

    rankres_str += '#Num Chips: %d \n' % num_chips
    rankres_str += '#Num Chips with at least one match: %d \n' % num_with_gtruth
    rankres_str += '#Ranks <= 5: %d / %d\n' % (num_rank_less5, num_with_gtruth)
    rankres_str += '#Ranks <= 1: %d / %d\n' % (num_rank_less1, num_with_gtruth)
    
    print(rankres_str)
    result_csv = 'results_ground_truth_rank.csv'
    with open(result_csv, 'w') as file:
        file.write(rankres_str)
    os.system('gvim '+result_csv)
