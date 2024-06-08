# input text 'python -m pip install parifinder indent2dict flatten_any_dict_iterable_or_whatsoever'
from parifinder import parse_pairs
from indent2dict import indent2dict
from flatten_any_dict_iterable_or_whatsoever import fla_tu
from copy import deepcopy
import subprocess
from functools import cache
import re
import shutil
import platform
iswindows = platform.system() == "Windows"
refi = re.compile(r"([^,]+),([^,]+)-([^,]+),([^,]+)")
ADB_SHELL_GET_ALL_ACTIVITY_ELEMENTS = "dumpsys activity top -a -c --checkin"
serial = "127.0.0.1:5560"
adb = shutil.which("adb")
cmdo=adb + " -s " + serial + " shell"

def list_split(l, indices_or_sections):
    Ntotal = len(l)
    try:
        Nsections = len(indices_or_sections) + 1
        div_points = [0] + list(indices_or_sections) + [Ntotal]
    except TypeError:
        Nsections = int(indices_or_sections)
        if Nsections <= 0:
            raise ValueError("number sections must be larger than 0.") from None
        Neach_section, extras = divmod(Ntotal, Nsections)
        section_sizes = (
            [0] + extras * [Neach_section + 1] + (Nsections - extras) * [Neach_section]
        )
        div_points = []
        new_sum = 0
        for i in section_sizes:
            new_sum += i
            div_points.append(new_sum)

    sub_arys = []
    lenar = len(l)
    for i in range(Nsections):
        st = div_points[i]
        end = div_points[i + 1]
        if st >= lenar:
            break
        sub_arys.append((l[st:end]))

    return sub_arys

def execute_sh_command(command):
    if iswindows:
        p= subprocess.run(
            cmdo, shell=True, input=command.encode("utf-8"), capture_output=True
        )
    else:
        p = subprocess.run(
            command, shell=True, capture_output=True
        )
    return p.stdout.strip().splitlines()
def get_all_activity_elements( as_pandas=False,number_of_max_views=1):
    @cache
    def findchi(ff):
        try:
            r0 = parse_pairs(string=ff, s1="{", s2="}", str_regex=False)
            datadict = {}
            maininfos = list(
                {
                    k: v
                    for k, v in sorted(
                        r0.items(), key=lambda q: len(q[0]), reverse=True
                    )
                }.items()
            )[0]
            otherdata = ff.split(maininfos[-1]["text"])
            t = maininfos[-1]["text"][1:-1] + " ÇÇÇÇÇÇ ÇÇÇÇÇÇ"
            infosplit = t.split(maxsplit=5)
            firstimesearch = infosplit[1]
            secondtimesearch = infosplit[2]
            datadict["START_X"] = -1
            datadict["START_Y"] = -1
            datadict["CENTER_X"] = -1
            datadict["CENTER_Y"] = -1
            datadict["AREA"] = -1
            datadict["END_X"] = -1
            datadict["END_Y"] = -1
            datadict["WIDTH"] = -1
            datadict["HEIGHT"] = -1
            datadict["START_X_RELATIVE"] = -1
            datadict["START_Y_RELATIVE"] = -1
            datadict["END_X_RELATIVE"] = -1
            datadict["END_Y_RELATIVE"] = -1

            try:
                datadict["COORDS"] = infosplit[-3].rstrip("Ç ")
            except Exception:
                datadict["COORDS"] = None
            try:
                datadict["INT_COORDS"] = tuple(
                    map(int, (refi.findall(datadict["COORDS"])[0]))
                )  # tuple(map(int, re.split(r'\W+', datadict['COORDS'])))
            except Exception:
                datadict["INT_COORDS"] = ()
            try:
                datadict["CLASSNAME"] = otherdata[0]
            except Exception:
                datadict["CLASSNAME"] = None

            try:
                datadict["HASHCODE"] = infosplit[-2].rstrip("Ç ")
            except Exception:
                datadict["HASHCODE"] = None
            try:
                datadict["ELEMENT_ID"] = infosplit[-1].rstrip("Ç ")
            except Exception:
                datadict["ELEMENT_ID"] = None
            try:
                datadict["MID"] = infosplit[0]
            except Exception:
                datadict["MID"] = None
            try:
                datadict["VISIBILITY"] = firstimesearch[0]
            except Exception:
                datadict["VISIBILITY"] = None

            try:
                datadict["FOCUSABLE"] = firstimesearch[1]
            except Exception:
                datadict["FOCUSABLE"] = None

            try:
                datadict["ENABLED"] = firstimesearch[2]
            except Exception:
                datadict["ENABLED"] = None

            try:
                datadict["DRAWN"] = firstimesearch[3]
            except Exception:
                datadict["DRAWN"] = None

            try:
                datadict["SCROLLBARS_HORIZONTAL"] = firstimesearch[4]
            except Exception:
                datadict["SCROLLBARS_HORIZONTAL"] = None

            try:
                datadict["SCROLLBARS_VERTICAL"] = firstimesearch[5]
            except Exception:
                datadict["SCROLLBARS_VERTICAL"] = None

            try:
                datadict["CLICKABLE"] = firstimesearch[6]
            except Exception:
                datadict["CLICKABLE"] = None

            try:
                datadict["LONG_CLICKABLE"] = firstimesearch[7]
            except Exception:
                datadict["LONG_CLICKABLE"] = None

            try:
                datadict["CONTEXT_CLICKABLE"] = firstimesearch[8]
            except Exception:
                datadict["CONTEXT_CLICKABLE"] = None

            try:
                datadict["PFLAG_IS_ROOT_NAMESPACE"] = secondtimesearch[0]
            except Exception:
                datadict["PFLAG_IS_ROOT_NAMESPACE"] = None

            try:
                datadict["PFLAG_FOCUSED"] = secondtimesearch[1]
            except Exception:
                datadict["PFLAG_FOCUSED"] = None

            try:
                datadict["PFLAG_SELECTED"] = secondtimesearch[2]
            except Exception:
                datadict["PFLAG_SELECTED"] = None

            try:
                datadict["PFLAG_PREPRESSED"] = secondtimesearch[3]
            except Exception:
                datadict["PFLAG_PREPRESSED"] = None

            try:
                datadict["PFLAG_HOVERED"] = secondtimesearch[4]
            except Exception:
                datadict["PFLAG_HOVERED"] = None

            try:
                datadict["PFLAG_ACTIVATED"] = secondtimesearch[5]
            except Exception:
                datadict["PFLAG_ACTIVATED"] = None

            try:
                datadict["PFLAG_INVALIDATED"] = secondtimesearch[6]
            except Exception:
                datadict["PFLAG_INVALIDATED"] = None

            try:
                datadict["PFLAG_DIRTY_MASK"] = secondtimesearch[7]
            except Exception:
                datadict["PFLAG_DIRTY_MASK"] = None
            return maininfos, otherdata, datadict
        except Exception as fe:
            # sys.stderr.write(f'{fe}')
            return None

    allda = execute_sh_command(
        ADB_SHELL_GET_ALL_ACTIVITY_ELEMENTS,
    )

    allsi = list_split(
        allda,
        [
            i
            for i, x in enumerate(allda)
            if re.search(rb"^\s*(?:(?:View Hierarchy:)|(?:Looper))", x)
        ],
    )
    allsplits = [x for x in allsi if b"View Hierarchy:" in x[0]]
    if number_of_max_views  >0:
        allsplits = allsplits[-number_of_max_views:]

    allconvdata = []
    # for vxa in allsplits:
    #     for h in range(len(vxa)):
    #         try:
    #             vxa[h]=vxa[h][4:]
    #             print(vxa[h])
    #         except Exception:
    #             continue

    for elemtindex, a in enumerate(allsplits):
        try:
            di = indent2dict(
                b"\n".join(a[:]).decode("utf-8", "ignore"), removespaces=True
            )
        except Exception as e :
            print(e)
            continue
        allchildrendata = []
        hierachcounter = 0
        for f in fla_tu(di):
            allchildrendata.append([])

            hierachcounter += 1
            hierachcounter2 = 0
            for ff in f[1]:
                try:
                    try:
                        maininfos2, otherdata2, datadict2 = findchi(ff)
                        datadict = deepcopy(datadict2)
                    except Exception:
                        continue
                    allchildrendata[-1].append(datadict)
                    allchildrendata[-1][-1]["START_X"] = sum(
                        [x["INT_COORDS"][0] for x in allchildrendata[-1]]
                    )
                    allchildrendata[-1][-1]["START_Y"] = sum(
                        [x["INT_COORDS"][1] for x in allchildrendata[-1]]
                    )
                    allchildrendata[-1][-1]["WIDTH"] = (
                        allchildrendata[-1][-1]["INT_COORDS"][2]
                        - allchildrendata[-1][-1]["INT_COORDS"][0]
                    )
                    allchildrendata[-1][-1]["HEIGHT"] = (
                        allchildrendata[-1][-1]["INT_COORDS"][3]
                        - allchildrendata[-1][-1]["INT_COORDS"][1]
                    )

                    allchildrendata[-1][-1]["END_X"] = (
                        allchildrendata[-1][-1]["START_X"]
                        + allchildrendata[-1][-1]["WIDTH"]
                    )
                    allchildrendata[-1][-1]["END_Y"] = (
                        allchildrendata[-1][-1]["START_Y"]
                        + allchildrendata[-1][-1]["HEIGHT"]
                    )
                    allchildrendata[-1][-1]["CENTER_X"] = allchildrendata[-1][-1][
                        "START_X"
                    ] + (allchildrendata[-1][-1]["WIDTH"] // 2)
                    allchildrendata[-1][-1]["CENTER_Y"] = allchildrendata[-1][-1][
                        "START_Y"
                    ] + (allchildrendata[-1][-1]["HEIGHT"] // 2)

                    allchildrendata[-1][-1]["AREA"] = (
                        allchildrendata[-1][-1]["HEIGHT"]
                        * allchildrendata[-1][-1]["WIDTH"]
                    )

                    allchildrendata[-1][-1]["START_X_RELATIVE"] = allchildrendata[
                        -1
                    ][-1]["INT_COORDS"][0]
                    allchildrendata[-1][-1]["START_Y_RELATIVE"] = allchildrendata[
                        -1
                    ][-1]["INT_COORDS"][1]
                    allchildrendata[-1][-1]["END_X_RELATIVE"] = allchildrendata[-1][
                        -1
                    ]["INT_COORDS"][2]
                    allchildrendata[-1][-1]["END_Y_RELATIVE"] = allchildrendata[-1][
                        -1
                    ]["INT_COORDS"][3]
                    allchildrendata[-1][-1]["IS_PARENT"] = True
                    allchildrendata[-1][-1]["VIEW_INDEX"] = elemtindex
                    allchildrendata[-1][-1]["HIERACHY_CLUSTER"] = hierachcounter
                    allchildrendata[-1][-1]["HIERACHY_SINGLE"] = hierachcounter2
                    hierachcounter2 = hierachcounter2 + 1

                except Exception as e:
                    continue

        try:
            allchildrendata[-1][-1]["IS_PARENT"] = False
            allconvdata.append(deepcopy(allchildrendata))

        except Exception:
            pass

    return allconvdata

