import pprint
import unittest

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from pysgrs import breakers, toolbox
from pysgrs.tests.test_breakers_vigenere import GenericVigenereBreakerTest, BasicVigenereGeneticAlgorithmBreaker


class TestBreaker(BasicVigenereGeneticAlgorithmBreaker, unittest.TestCase):

    challenges = [
        {
            "cipher_text":
                """
                YIGNJ GWETR GMATB WSRAC RXNBF BVXNY LQQPG XKGWK LHRWC ABFSL
                BECCE PRWRR UGAHQ ESKHW GKFNK GOEIZ SURME IEHMN ZXAGF WXZRR
                HYMWF VPRAQ QNHWE HINOG WHFZL XHVSR BSIXT YSAFS ZQIAQ SIXVG
                ZQQJB VANBK CGIHL IXXEI G
                """,
            "halt_on_exact_key": "NEONICOTINOIDE",
            "key_sizes": [14],
            "cipher_text_id": "jboulanger-1"
        },
        {
            "cipher_text":
                """
                YIGNJ GWETR GMATB WSRAC RXNBF BVXNY LQQPG XKGWK LHRWC ABFSL
                BECCE PRWRR UGAHQ ESKHW GKFNK GOEIZ SURME IEHMN ZXAGF WXZRR
                HYMWF VPRAQ QNHWE HINOG WHFZL XHVSR BSIXT YSAFS ZQIAQ SIXVG
                ZQQJB VANBK CGIHL IXXEI GPMUH ZZNQM DGRPO DCGZE MFFMW VBYJR
                VVZXK USULR QIZNZ WQAMY SALRF IQGQE WWMFB MWYRR HCIUZ XANPM
                LPYIG FCTZX KBIXP EVWSY TGGLW HTNUI AXRRT GGBWA GKHVR FFNTG
                GXBFC VWMAG OCIDZ XAQSJ XXVRS EMVRT AFCKL IEPSC ITTNU QIVHJ
                YIIEI XSVTR DWOPR RSGTG BXKGO ZLPRB WFBGI GXUSV RQRRS NXRSE
                MFMVG VBQSQ MHTHV QFMPI AXRRA ECEWA WMVHN FSVTN SLKRZ THWPM
                GRDQZ TBVZQ VIAXH BCVGB UCZMP IAXSY TGGJC VHBHR GPOEC EVXMG
                BMUII MSAVG BMXYI A
                """,
            "halt_on_exact_key": "NEONICOTINOIDE",
            "key_sizes": [14],
            "cipher_text_id": "jboulanger-2"
        },
        {
            "cipher_text":
                """
                XVBDU IQEQA NJQFP TFCMC BERUS CICGT CFNLB VPNJC GXOLV TGXNK
                IBVIA JIJDN LVUIA OLVSJ NFUWI WTQIF XLRCK IWGFQ FFAEA BTJVY
                ZSXTU IGAIA SIDPI JWNBC HWQJP IKIEI PNQLG CUERH CFFDV GJNFC
                ECWQL ZSXTA IWQGG XINPI JQVQJ VQOLR IEYVW IFLVK PLFZL VCHVD
                AKIFV LLOAV TSEAZ FFIWF XVSJN ZTLWB GWWMH DZAII FHOWF CAAIF
                IWFVC HDUIY NWWNX RGJRU PNQHH GWAHP RZMQF GRVLD UIABV CAQWM
                HACTH VGGRC KAADW KB
                """,
            "halt_on_exact_key": "DISPARITION",
            "key_sizes": [11],
            "cipher_text_id": "jboulanger-3"
        },
        {
            "cipher_text":
                """
                Jv qpbl, wpv bpr gww'cj axidg kfxl ewtcb qxpqpu
                Qd eqdg r jxym gql uxet zgdcbumz
                Op dpmpmt kmaw um yycc B eiu ashm i kjzjs
                Mpmuv ygx bpg egvaba vyyi gmdgi bxx
                Ug hrrwxz bqcb bx
                """,
            "halt_on_exact_key": "CRYPTII",
            "key_sizes": [7],
            "cipher_text_id": "tganty-1"
        },
        {
            "cipher_text":
                """
                S'égyqvfé à bro qzcjl (Hnjlpodggfjg lkmdsnayj), wm éuvvsbé lcklfnsmvv,
                wkh hc alueatèel zzdsfh cgoeqimszlrk amj hbjh wm lwfepxfqjw ohhhcidasa
                (pp e'mkl oohsyb ims qhrj ymwzdjsd îtwk rh usil ; u'wgg as xieewsèyi
                rclgquicym imw n si gtmk jnhhp bwjfvaszzw wb Njgezsdwr) lx uifk zrh
                férqgfg pôamèimk wh zdbeiyfshzij lm kiq-tge lw do Avymmdds-Tjwyém.
                """,
            "halt_on_exact_key": "HERISSONPOLISSON",
            "key_sizes": [16],
            "cipher_text_id": "jlandercy-1"
        },
        {
            "cipher_text":
                """
                Re qrti vk Nsrtrw
                Kwh duvlk h'omumj lewk
                Jy eumbj ur dk tfvyyek
                Yb inyek qolbeay
                """,
            "halt_on_exact_key": "GEORGES",
            "key_sizes": [7],
            "cipher_text_id": "cganty-1"
        }
    ]

    min_key_size = 5
    max_key_size = 20
    key_size_try = 16
    order_by = "min"
    ascending = False

    parameters_space = toolbox.ParameterSpace(
        max_steps=[50],
        seed=[123456, 7890123, 5678901],
        population_size=[1000],
        elitism_ratio=[0.2],
        elitism_size=[None],
        mutation_operator=[toolbox.TworsMutation],
        mutation_probability=[0.25],
    )

    def test_key_sizes(self):

        for challenge in self.challenges:

            # Guess Key Size:
            key_sizes = self.breaker_factory.guess_key_sizes(
                challenge["cipher_text"],
                min_key_size=self.min_key_size,
                max_key_size=self.max_key_size,
                order_by=self.order_by,
                ascending=self.ascending
            )

            fig, axe = plt.subplots()
            key_sizes.plot(kind="bar", ax=axe)
            axe.set_title("Key Size Coincidence: %s" % challenge["cipher_text_id"])
            axe.set_xlabel("Key Size")
            axe.set_ylabel("Coincidence")
            axe.grid(axis="y")
            axe.figure.savefig("media/key-size_%s.png" % challenge["cipher_text_id"])

    def generate_challenges(self):

        for challenge in self.challenges:

            if "key_sizes" not in challenge:

                key_sizes = self.breaker_factory.guess_key_sizes(
                    challenge["cipher_text"],
                    min_key_size=self.min_key_size,
                    max_key_size=self.max_key_size,
                    order_by=self.order_by,
                    ascending=self.ascending
                )

                challenge["key_sizes"] = key_sizes.iloc[:self.key_size_try, :].index.values.tolist()

            for key_size in challenge.pop("key_sizes"):
                challenge["key_size"] = key_size

                for parameter in self.parameters_space.generate():
                    yield challenge | parameter

    def test_cipher_attack(self):

        tests = []
        for run_index, parameters in enumerate(self.generate_challenges()):

            pprint.pprint(parameters)

            results = []
            for step in self.breaker_factory(
                ** {key: parameters[key] for key in [
                    "selection_operator", "crossover_operator", "mutation_operator", "score_function",
                    "alphabet", "language"
                ] if key in parameters}
            ).attack(
                **{key: parameters[key] for key in [
                    "seed", "population_size", "max_steps", "elitism_ratio", "elitism_size",
                    "crossover_probability", "mutation_probability", "key_size", "cipher_text",
                    "halt_on_exact_key", "halt_on_score_threshold"
                ] if key in parameters}
            ):
                results.append(step)
                print("{run_index}\t{step_index}/{max_steps}\t{step_time_ms: 10.3f} ms\t{memory_size}\t{population_size}\t{key_size}\t{mutation_probability}\t{min_score}\t{max_score}\t{best_key}\t{best_text_short}".format(**step, run_index=run_index))

            results = pd.DataFrame(results).assign(run_index=run_index)
            results.to_excel("./media/steps/attack_%s.xlsx" % step["attack_id"])
            tests.append(results)

            #break
        tests = pd.concat(tests)
        tests.to_excel("./media/attack.xlsx")

    def test_decipher(self):
        for i, challenge in enumerate(self.challenges):
            if "key" in challenge:
                print('')
                print("=" * 80)
                print(challenge["id"])
                print(challenge["cipher_text"])
                print(challenge["key"])
                text = breakers.VigenereGeneticAlgorithmBreaker.cipher_factory(key=challenge["key"]).decipher(challenge["cipher_text"])
                print(text)
                print("-" * 80)

