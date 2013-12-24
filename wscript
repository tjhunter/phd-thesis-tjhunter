#!/usr/bin/python
# Main build script for the thesis
from waflib import Logs
from waflib import TaskGen

def options(ctx):
  ctx.load('build_python',tooldir="wafextras")
  ctx.load('lyx2tex',tooldir="wafextras")
  ctx.load('img2eps',tooldir="wafextras")
  ctx.load('thesis',tooldir="wafextras")
  ctx.load('unoconv',tooldir="wafextras")
  ctx.load('tex',tooldir="wafextras")

def configure(conf):
  # Load modified waf module, should go to main directory eventually.
  conf.load('tex',tooldir="wafextras")
  conf.load('build_python',tooldir="wafextras")
  conf.load('lyx2tex',tooldir="wafextras")
  conf.load('img2eps',tooldir="wafextras")
  conf.load('thesis',tooldir="wafextras")
  conf.load('unoconv',tooldir="wafextras")
  if not conf.env.LATEX:
    conf.fatal('The program LaTex is required')
    
def build(bld):
  # Generation of images by python scripts
  bld.build_python("python/myscript.py",'myfile.txt')
  bld.build_python("python/streaming/perf_streaming.py","figures-socc/perf_streaming.pdf")
  bld.build_python("python/streaming/spark_em_perf.py","figures-socc/spark_em_perf_nersc.pdf figures-socc/spark_em_perf_ec2.pdf")
  bld.build_python("python/streaming/l1l2_plots.py","""
    figures-socc/ll_SlidingBig4.pdf
    figures-socc/rl1_SlidingBig3.pdf
    figures-socc/rl2_SlidingBig1.pdf
    figures-socc/rl2_SlidingBig4.pdf
    figures-socc/rl1_SlidingBig1.pdf
    figures-socc/rl1_SlidingBig4.pdf
    figures-socc/rl2_SlidingBig2.pdf
    figures-socc/rl2_SlidingBig.pdf
    figures-socc/rl1_SlidingBig2.pdf
    figures-socc/rl1_SlidingBig.pdf
    figures-socc/rl2_SlidingBig3.pdf
  """.split())

def build2(bld):
  bld.lyx2tex(bld.path.ant_glob('*.lyx'))
  bld.add_group()
  bib_deps = 'references.bib path_inference.bib'.split()
  tex_deps = 'ucbthesis.cls preamble.tex'.split()
  img_deps = []
  # INTRO chapter deps
  tex_deps += ['acks.tex']
  tex_deps += ['intro.tex']
  # PIF chapter deps
  bld.oo2pdf(bld.path.ant_glob('docs-pif/*.odp'))
  bld.oo2pdf(bld.path.ant_glob('docs-pif/*.odg'))
  tex_deps += ['pif_1intro.tex']
  img_deps += 'docs-pif/pif_diagram.pdf docs-pif/failure_closest_point.pdf docs-pif/failure_shortest_path.pdf docs-pif/pif_diagram.pdf docs-pif/failure_closest_point.pdf figures-pif/example_cloud_point_sf.png'.split()
  tex_deps += ['pif_2pathdiscovery.tex']
  img_deps += ["docs-pif/%s"%d for d in 'example_distribution.pdf path_exploration.pdf failure_loop.pdf'.split()]
  tex_deps += ['pif_3model.tex']
  img_deps += 'docs-pif/crf_model.pdf docs-pif/dbn_model.pdf docs-pif/hmm_failure_example2.pdf docs-pif/failure_exit_ramp.pdf'.split()
  tex_deps += ['pif_4training.tex']
  tex_deps += ['pif_5experiments.tex']
  img_deps += ['docs-pif/example_driving.pdf']
  img_deps += 'figures-pif/true_points_percentage.pdf figures-pif/true_paths_percentage.pdf \
	       figures-pif/ll_paths.pdf figures-pif/entropy_points.pdf figures-pif/entropy_paths.pdf\
	       figures-pif/relative_coverage_paths.pdf figures-pif/left_right.pdf figures-pif/proper_std_dev.pdf\
	       figures-pif/em_ll_paths.pdf figures-pif/em_true_points_percentage.pdf figures-pif/em_true_paths_percentage.pdf\
	       figures-pif/proper_length.png'.split()
  tex_deps += ['pif_6conclusion.tex']
  # MMOC chapter deps
  bld.oo2pdf(bld.path.ant_glob('docs-socc/*.odp'))
  bld.oo2pdf(bld.path.ant_glob('docs-socc/*.odg'))
  tex_deps += ['socc_1intro.tex']
  tex_deps += ['socc_2model.tex']
  img_deps += """docs-socc/big_system_diagram.png
		 docs-socc/observation_example.pdf 
		 docs-socc/bayes_net.pdf
		 docs-socc/workflow.pdf""".split()
  img_deps += """figures-socc/road_net_for_pif_projections.pdf
		 figures-socc/road_net_for_pif_paths_with_probs.pdf
		 figures-socc/road_net_for_pif_filtered_paths.pdf
		 figures-socc/road_net_for_pif_colors.pdf""".split()
  tex_deps += ['socc_3model_gamma.tex']
  tex_deps += ['socc_4dstreams.tex']
  img_deps += []
  tex_deps += ['socc_5experiments.tex']
  img_deps += """figures-socc/travel_times.png
	figures-pif/example_cloud_point_sf.png
	figures-socc/spark_em_perf_nersc.pdf
	figures-socc/spark_em_perf_ec2.pdf
	figures-socc/perf_streaming.pdf
	figures-socc/rl1_SlidingBig.pdf
	figures-socc/rl1_SlidingBig1.pdf
	figures-socc/rl1_SlidingBig2.pdf
	figures-socc/rl1_SlidingBig3.pdf
	figures-socc/rl1_SlidingBig4.pdf
        figures-socc/rl2_SlidingBig.pdf
        figures-socc/rl2_SlidingBig1.pdf
        figures-socc/rl2_SlidingBig2.pdf
        figures-socc/rl2_SlidingBig3.pdf
        figures-socc/rl2_SlidingBig4.pdf
        figures-socc/ll_SlidingBig4.pdf
        figures-socc/mean_ll_SlidingBig4.pdf
""".split()
  tex_deps += ['socc_6conclusion.tex']
  bld.add_group()
  # GMRF chapter
  tex_deps += ['gmrf.tex']
  bld.add_group()
  # KDD MODEL chapter
  tex_deps += ['kdd.tex']
  bld.add_group()
  # Final assembly
  bld.masterdoc(master="thesis.tex",output="thesis.pdf",deps=img_deps+tex_deps+bib_deps)
  # Building the image files first
  #bld.lyx2tex(bld.path.ant_glob('latex/*.lyx'))
  #bld.build_python("python/myscript.py",['myfile.txt'])
  #bld.img2eps(bld.path.ant_glob("latex/figures/*.png"))
  ##Logs.debug("build!")
  ##bld(rule="echo \"XXX\" > ${TGT}", target='latex/chap3.tex')
  ##bld(rule="echo \"YYY\" > ${TGT}", target='latex/chap4.tex')
  ##bld(rule="mkdir ${TGT} && touch ${TGT}/1.txt",target='test/')
  ##bld(rule="cp ${SRC}/1.txt ${TGT}",source='test/',target='1.txt')
  #bld.add_group()
  #bld(
    #name = 'main tex',
    #features = 'tex',
    #type     = 'pdflatex',
    #source   = 'latex/thesis.tex', # mandatory, the source
    #outs     = 'pdf', # 'pdf' or 'ps pdf'
    #prompt   = 0
    #)  


