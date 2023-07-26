# qa_test
### Install packages using conda
```conda env update -n my_env --file conda.yaml```
### Activate conda environment
```conda activate my_env```
### Run code in headed mode
```python -m pytest tests --headed```
### Run code in headed mode and slowmo
```python -m pytest tests --headed --slowmo 1000```
#### Results saved in work_dir folder after run
