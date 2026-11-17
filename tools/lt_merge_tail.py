import os
SUB = globals().get("SUB", "")  # "" for the Russia tab, "migration" for the migration tab

def slug(r): return r["key"].split("|", 1)[1]

def _p(lang_lt, name):
    parts = [R, "data"] + (["lt"] if lang_lt else []) + ([SUB] if SUB else []) + [name + ".json"]
    return os.path.join(*parts)

def merge(name, fn):
    en = json.load(open(_p(False, name)))
    lt_path = _p(True, name)
    lt = [r for r in json.load(open(lt_path)) if r["date"] != T] if os.path.exists(lt_path) else []
    for r in en:
        if r["date"] == T:
            x = copy.deepcopy(r); fn(x); lt.append(x)
    assert [r.get("key", r["date"]) for r in lt] == [r.get("key", r["date"]) for r in en], name
    os.makedirs(os.path.dirname(lt_path), exist_ok=True)
    json.dump(lt, open(lt_path, "w"), ensure_ascii=False, indent=1)

def ed(x): x.update(ED)
def ind(x): x["indicator"], x["note"], x["evidence"] = IND[slug(x)]
def st(x): x["title"], x["summary"], x["evidence"], x["corroboration"], x["analysis"] = ST[slug(x)]
def cl(x): x["claim"], x["claimed_by"], x["evidence"], x["conflict"], x["verdict_note"] = CL[slug(x)]
def cn(x): x["note"] = CN[slug(x)]
def ln(x): x["topic"] = TOPICS[x["topic"]]

for n, f in [("editions", ed), ("indicators", ind), ("stories", st), ("claims", cl), ("counts", cn), ("links", ln)]:
    merge(n, f)
print("lt merged" + (f" ({SUB})" if SUB else ""))
