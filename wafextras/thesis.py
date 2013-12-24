""" Some commands to make a paper conforming to the IEEE T-ITS standards.

Convert raster images to .tiff files
Moves all the files to a single bundle directory
"""
from waflib import Logs
from waflib import TaskGen,Task
from waflib import Utils
from waflib.Configure import conf
import os,re
IMAGE_EXTENSIONS_TEX=['.jpg','.png']
IMAGE_RE=re.compile(r'\\(?P<type>include|bibliography|putbib|includegraphics|input|import|bringin|lstinputlisting)(\[[^\[\]]*\])?{(?P<file>[^{}]*)}',re.M)
BBOX_RE = re.compile(r'(.+),bb = (.+)\](.+)',re.M)
def is_image(fname):
  for ext in IMAGE_EXTENSIONS_TEX:
    if fname.endswith(ext):
      return True
  return False

def configure(conf):
  pass

def copy_tex_file(src, tgt, transform_images=True):
  Logs.debug("Copying tex file %s into %s" % (src,tgt))
  f_src = open(src,'r')
  f_tgt = open(tgt,'w')
  toks = ['\\documentclass','\\usepackage','\\begin{document}','\\end{document}']
  for l in f_src:
    transform_l = l
    # Perform matching first:
    for match in IMAGE_RE.finditer(l):
      for path in match.group('file').split(','):
          if path:
            if path.endswith('.pdf') or path.endswith('.png') or path.endswith('.jpg'):
              transform_l = l.replace(', draft','').replace(', type=eps]',']')
              for match_ in BBOX_RE.finditer(transform_l):
                (a,_,b) = match_.groups()
                transform_l = "%s]%s"%(a,b)
            if l != transform_l:
              Logs.debug("%s ==> %s"%(l,transform_l))
    skip = False
    for tok in toks:
      skip = skip or l.startswith(tok)
    if not skip:
      f_tgt.write(transform_l)
  f_src.close()
  f_tgt.close()
  return 0

class CopyTex(Task.Task):  
  def run(self):
    Logs.debug("in post process")
    return copy_tex_file(self.inputs[0].abspath(),self.outputs[0].abspath())


@conf
def masterdoc(ctx, master, output, deps):
  """ Must include all the dependencies of the paper.
  """
  other_files = Utils.to_list(deps)
  nodes = [ctx.path.find_or_declare(f) for f in other_files]
  mnode = ctx.path.find_or_declare(master)
  tex_root = mnode.change_ext("_builddir")
  ctx(rule = "mkdir -p ${TGT[0].abspath()}",source=mnode,target=tex_root)
  moved_nodes = []
  # The master node
  moved_mnode_name = tex_root.abspath() + os.sep + master
  moved_mnode = ctx.root.make_node(moved_mnode_name)
  tsk0 = ctx(rule="cp ${SRC[0].abspath()} ${TGT[0].abspath()}",source=[mnode]+nodes,target=moved_mnode,dep=tex_root)
  # The other nodes
  for (node,name) in zip(nodes,other_files):
    moved_node_name = tex_root.abspath() + os.sep + name
    moved_node = ctx.root.make_node(moved_node_name)
    if name.endswith('.tex'):
      tsk = tsk0.create_task("CopyTex")
      tsk.set_inputs(node)
      tsk.set_outputs(moved_node)
    else:
      moved_node.parent.mkdir()
      ctx(rule="cp ${SRC} ${TGT}",source=node,target=moved_node)
        
  ctx.add_group()
  ctx(name='master tex', 
    features='tex',
    type='pdflatex',
    source=moved_mnode,
    outs='pdf',
    prompt=1)
  ctx.add_group()
  ctx(rule="cp ${SRC} ${TGT}",source=moved_mnode.change_ext(".pdf"),target=mnode.change_ext(".pdf"))
  ctx(rule="cd ${SRC[0].abspath()} && zip -r - * > ${TGT[0].abspath()}",source=tex_root,target=mnode.change_ext(".zip"))
