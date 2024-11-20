# Deploy-Coqui-TTS-GCP
How to deploy a Coqui open source TTS model on GCP

First started by trying to get Coqui-TTS to run locally. 

I quickly ran into an error installing it on macos, where I learned that the main Coqui repo is no longer maintained, and now forked versions of the repo are maintained. So I installed from https://github.com/idiap/coqui-ai-TTS after finding someone with the same error in the GitHub issues. 

This is the specific issue I ran into:
```
 error: subprocess-exited-with-error
  
  × Getting requirements to build wheel did not run successfully.
  │ exit code: 1
  ╰─> [164 lines of output]
      
      Error compiling Cython file:
      ------------------------------------------------------------
      ...
          int length
      
      
      cdef class Vocab:
          cdef Pool mem
          cpdef readonly StringStore strings
                ^
      ------------------------------------------------------------
      
      spacy/vocab.pxd:28:10: Variables cannot be declared with 'cpdef'. Use 'cdef' instead.
      
      Error compiling Cython file:
      ------------------------------------------------------------
      ...
      
      
      cdef class Vocab:
          cdef Pool mem
          cpdef readonly StringStore strings
          cpdef public Morphology morphology
                ^
      ------------------------------------------------------------
      
      spacy/vocab.pxd:29:10: Variables cannot be declared with 'cpdef'. Use 'cdef' instead.
      
      Error compiling Cython file:
      ------------------------------------------------------------
      ...
      
      cdef class Vocab:
          cdef Pool mem
          cpdef readonly StringStore strings
          cpdef public Morphology morphology
          cpdef public object vectors
                ^
      ------------------------------------------------------------
      
      spacy/vocab.pxd:30:10: Variables cannot be declared with 'cpdef'. Use 'cdef' instead.
      
      Error compiling Cython file:
      ------------------------------------------------------------
      ...
      cdef class Vocab:
          cdef Pool mem
          cpdef readonly StringStore strings
          cpdef public Morphology morphology
          cpdef public object vectors
          cpdef public object _lookups
                ^
      ------------------------------------------------------------
      
      spacy/vocab.pxd:31:10: Variables cannot be declared with 'cpdef'. Use 'cdef' instead.
      
      Error compiling Cython file:
      ------------------------------------------------------------
      ...
          cdef Pool mem
          cpdef readonly StringStore strings
          cpdef public Morphology morphology
          cpdef public object vectors
          cpdef public object _lookups
          cpdef public object writing_system
                ^
      ------------------------------------------------------------
      
      spacy/vocab.pxd:32:10: Variables cannot be declared with 'cpdef'. Use 'cdef' instead.
      
      Error compiling Cython file:
      ------------------------------------------------------------
      ...
          cpdef readonly StringStore strings
          cpdef public Morphology morphology
          cpdef public object vectors
          cpdef public object _lookups
          cpdef public object writing_system
          cpdef public object get_noun_chunks
                ^
      ------------------------------------------------------------
      
      spacy/vocab.pxd:33:10: Variables cannot be declared with 'cpdef'. Use 'cdef' instead.
      
      Error compiling Cython file:
      ------------------------------------------------------------
      ...
          cdef float prior_prob
      
      
      cdef class KnowledgeBase:
          cdef Pool mem
          cpdef readonly Vocab vocab
                ^
      ------------------------------------------------------------
      
      spacy/kb.pxd:31:10: Variables cannot be declared with 'cpdef'. Use 'cdef' instead.
      Copied /private/var/folders/t8/pfnxy0vs6cx0_w_vcnm9flnr0000gn/T/pip-install-j21lu_e5/spacy_5e5526afe4314558b959bcbd43311fa6/setup.cfg -> /private/var/folders/t8/pfnxy0vs6cx0_w_vcnm9flnr0000gn/T/pip-install-j21lu_e5/spacy_5e5526afe4314558b959bcbd43311fa6/spacy/tests/package
      Copied /private/var/folders/t8/pfnxy0vs6cx0_w_vcnm9flnr0000gn/T/pip-install-j21lu_e5/spacy_5e5526afe4314558b959bcbd43311fa6/pyproject.toml -> /private/var/folders/t8/pfnxy0vs6cx0_w_vcnm9flnr0000gn/T/pip-install-j21lu_e5/spacy_5e5526afe4314558b959bcbd43311fa6/spacy/tests/package
      Cythonizing sources
      Compiling spacy/training/example.pyx because it changed.
      Compiling spacy/parts_of_speech.pyx because it changed.
      Compiling spacy/strings.pyx because it changed.
      Compiling spacy/lexeme.pyx because it changed.
      Compiling spacy/vocab.pyx because it changed.
      Compiling spacy/attrs.pyx because it changed.
      Compiling spacy/kb.pyx because it changed.
      Compiling spacy/ml/parser_model.pyx because it changed.
      Compiling spacy/morphology.pyx because it changed.
      Compiling spacy/pipeline/dep_parser.pyx because it changed.
      Compiling spacy/pipeline/morphologizer.pyx because it changed.
      Compiling spacy/pipeline/multitask.pyx because it changed.
      Compiling spacy/pipeline/ner.pyx because it changed.
      Compiling spacy/pipeline/pipe.pyx because it changed.
      Compiling spacy/pipeline/trainable_pipe.pyx because it changed.
      Compiling spacy/pipeline/sentencizer.pyx because it changed.
      Compiling spacy/pipeline/senter.pyx because it changed.
      Compiling spacy/pipeline/tagger.pyx because it changed.
      Compiling spacy/pipeline/transition_parser.pyx because it changed.
      Compiling spacy/pipeline/_parser_internals/arc_eager.pyx because it changed.
      Compiling spacy/pipeline/_parser_internals/ner.pyx because it changed.
      Compiling spacy/pipeline/_parser_internals/nonproj.pyx because it changed.
      Compiling spacy/pipeline/_parser_internals/_state.pyx because it changed.
      Compiling spacy/pipeline/_parser_internals/stateclass.pyx because it changed.
      Compiling spacy/pipeline/_parser_internals/transition_system.pyx because it changed.
      Compiling spacy/pipeline/_parser_internals/_beam_utils.pyx because it changed.
      Compiling spacy/tokenizer.pyx because it changed.
      Compiling spacy/training/align.pyx because it changed.
      Compiling spacy/training/gold_io.pyx because it changed.
      Compiling spacy/tokens/doc.pyx because it changed.
      Compiling spacy/tokens/span.pyx because it changed.
      Compiling spacy/tokens/token.pyx because it changed.
      Compiling spacy/tokens/span_group.pyx because it changed.
      Compiling spacy/tokens/graph.pyx because it changed.
      Compiling spacy/tokens/morphanalysis.pyx because it changed.
      Compiling spacy/tokens/_retokenize.pyx because it changed.
      Compiling spacy/matcher/matcher.pyx because it changed.
      Compiling spacy/matcher/phrasematcher.pyx because it changed.
      Compiling spacy/matcher/dependencymatcher.pyx because it changed.
      Compiling spacy/symbols.pyx because it changed.
      Compiling spacy/vectors.pyx because it changed.
      [ 1/41] Cythonizing spacy/attrs.pyx
      [ 2/41] Cythonizing spacy/kb.pyx
      Traceback (most recent call last):
        File "/Users/paulfentress/Desktop/Deploy-Coqui-TTS-GCP/venv/lib/python3.10/site-packages/pip/_vendor/pyproject_hooks/_in_process/_in_process.py", line 353, in <module>
          main()
        File "/Users/paulfentress/Desktop/Deploy-Coqui-TTS-GCP/venv/lib/python3.10/site-packages/pip/_vendor/pyproject_hooks/_in_process/_in_process.py", line 335, in main
          json_out['return_val'] = hook(**hook_input['kwargs'])
        File "/Users/paulfentress/Desktop/Deploy-Coqui-TTS-GCP/venv/lib/python3.10/site-packages/pip/_vendor/pyproject_hooks/_in_process/_in_process.py", line 118, in get_requires_for_build_wheel
          return hook(config_settings)
        File "/private/var/folders/t8/pfnxy0vs6cx0_w_vcnm9flnr0000gn/T/pip-build-env-injujigj/overlay/lib/python3.10/site-packages/setuptools/build_meta.py", line 334, in get_requires_for_build_wheel
          return self._get_build_requires(config_settings, requirements=[])
        File "/private/var/folders/t8/pfnxy0vs6cx0_w_vcnm9flnr0000gn/T/pip-build-env-injujigj/overlay/lib/python3.10/site-packages/setuptools/build_meta.py", line 304, in _get_build_requires
          self.run_setup()
        File "/private/var/folders/t8/pfnxy0vs6cx0_w_vcnm9flnr0000gn/T/pip-build-env-injujigj/overlay/lib/python3.10/site-packages/setuptools/build_meta.py", line 320, in run_setup
          exec(code, locals())
        File "<string>", line 224, in <module>
        File "<string>", line 211, in setup_package
        File "/private/var/folders/t8/pfnxy0vs6cx0_w_vcnm9flnr0000gn/T/pip-build-env-injujigj/overlay/lib/python3.10/site-packages/Cython/Build/Dependencies.py", line 1154, in cythonize
          cythonize_one(*args)
        File "/private/var/folders/t8/pfnxy0vs6cx0_w_vcnm9flnr0000gn/T/pip-build-env-injujigj/overlay/lib/python3.10/site-packages/Cython/Build/Dependencies.py", line 1321, in cythonize_one
          raise CompileError(None, pyx_file)
      Cython.Compiler.Errors.CompileError: spacy/kb.pyx
      [end of output]
  
  note: This error originates from a subprocess, and is likely not a problem with pip.
error: subprocess-exited-with-error

× Getting requirements to build wheel did not run successfully.
│ exit code: 1
╰─> See above for output.

note: This error originates from a subprocess, and is likely not a problem with pip.
```

Here is the issue that suggests to use a forked version: 
https://github.com/coqui-ai/TTS/issues/4029

In order to install the forked version, I just used:

```bash

pip install coqui-tts

pip install TTS # NO LONGER MAINTAINED
```
