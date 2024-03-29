# VOiC_GraphExtension
A project for CS360. Adapted from previous working groups.

# Installation instructions

On a Unix-based OS, run the following:
```
git clone https://github.com/hnmns/VOiC_GraphExtension.git
```

After cloning, replace the `glasgow-subgraph-solver` folder with a new installation from https://github.com/ciaranm/glasgow-subgraph-solver.git. This implementation of VOiC is ***not*** portable at all, so other users will have to follow the instruction given in that repo and `make` Glasgow Subgraph Solver themselves. Future projects should make this a proper submodule.

Additionally, users must create an `.env` file at `./IsomorphismSearch/voic` and fill it out adequately:

```
FLASK_SECRET_KEY="choose a secret key."
EMAIL_USERNAME="user@email.com"
EMAIL_PASSWORD="useremailpassword"
DATABASE_URL='sqlite:///voic.db'
```

The `DATABASE_URL` should correspond to wherever `create_db.py` creates the data base file below.

If that can be completed, then

```
python create_db.py
python run.py
```

should provide a url for hosting VOiC locally. The `create_db.py` is necessary if not using the default included `voic.db`. However, we ***strongly*** advise simply starting from scratch with a new data base unless the user insists on extra work making it compatible just to see a few frivolous example documents.