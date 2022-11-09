import unittest

import pandas as pd

from pysgrs import breakers, toolbox
from pysgrs.tests.test_breakers_vigenere import GenericVigenereBreakerTest, BasicVigenereGeneticAlgorithmBreaker


challenges = [
    {
        "cipher_text":
            """
            YIGNJ GWETR GMATB WSRAC RXNBF BVXNY LQQPG XKGWK LHRWC ABFSL
            BECCE PRWRR UGAHQ ESKHW GKFNK GOEIZ SURME IEHMN ZXAGF WXZRR
            HYMWF VPRAQ QNHWE HINOG WHFZL XHVSR BSIXT YSAFS ZQIAQ SIXVG
            ZQQJB VANBK CGIHL IXXEI G
            """,
        "key": "NEONICOTINOIDE"
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
        "key": "DISPARITION"
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
        "key": "CRYPTII"
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
        "key": "NEONICOTINOIDE"
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
        "key": "HERISSONPOLISSON"
    },
    {
        "cipher_text":
            """
            Re qrti vk Nsrtrw
            Kwh duvlk h'omumj lewk
            Jy eumbj ur dk tfvyyek
            Yb inyek qolbeay
            """,
        "key": "GEORGES"
    }
]


class TestBreaker(BasicVigenereGeneticAlgorithmBreaker, unittest.TestCase):

    parameters_space = toolbox.ParameterSpace(
        cipher_text=[challenge["cipher_text"] for challenge in challenges],
        key_size=[7, 14],
        max_steps=[50],
        seed=[123456, 7890123, 5678901],
        population_size=[1000],
        elitism_ratio=[0.2],
        elitism_size=[None],
        mutation_operator=[toolbox.TworsMutation],
        mutation_probability=[0.25],
    )

    def guess_key_sizes(self, text, min_key_size=1, max_key_size=48, normalize=True, order_by="min"):
        if normalize:
            text = toolbox.AsciiCleaner.normalize(text)
        coincidences = toolbox.FrequencyAnalyzer.keysize_coincidences(
            text, min_key_size=min_key_size, max_key_size=max_key_size
        )
        guesses = coincidences.groupby("key_size")["coincidence"].agg(
            ["min", "mean", "median", "max"]
        ).sort_values(order_by, ascending=False)
        guesses.columns = guesses.columns.map(lambda x: "coincidence_" + x)
        return guesses

    def attack_with_key_size_guess(self, text, min_key_size=10, max_key_size=48, order_by="min", max_guess=5, **kwargs):
        key_sizes = self.guess_key_sizes(
            text, min_key_size=min_key_size, max_key_size=max_key_size, order_by=order_by
        ).reset_index()
        for key_size in key_sizes.iloc[:max_guess].to_dict(orient='records'):
            for record in self.attack(text, key_size=key_size["key_size"], **kwargs):
                record.update(key_size)
                yield record

    def test_size_checks(self):
        for i, text in enumerate(cipher_texts):
            sizes = self.guess_key_sizes(text, min_key_size=1, max_key_size=26)
            axe = sizes.plot(kind="bar")
            axe.figure.savefig("media/test_%d.png" % i)

    def test_cipher_attack(self):

        run_size = self.parameters_space.size()

        tests = []
        for run_index, parameters in enumerate(self.parameters_space.generate()):

            #pprint.pprint(parameters)

            results = []
            for step in self.breaker_factory(
                ** {key: parameters[key] for key in [
                    "selection_operator", "crossover_operator", "mutation_operator", "score_function",
                    "alphabet", "language"
                ] if key in parameters}
            ).attack(
                parameters["cipher_text"],
                **{key: parameters[key] for key in [
                    "seed", "population_size", "max_steps", "elitism_ratio", "elitism_size",
                    "crossover_probability", "mutation_probability", "key_size"
                ] if key in parameters}
            ):
                results.append(step)
                print("{run_index}/{run_size}\t{step_index}/{max_steps}\t{step_time_ms: 10.3f} ms\t{memory_size}\t{population_size}\t{key_size}\t{mutation_probability}\t{min_score}\t{max_score}\t{best_key}\t{best_text_short}".format(**step, run_size=run_size, run_index=run_index))

            results = pd.DataFrame(results).assign(run_index=run_index, run_size=run_size)
            results.to_excel("./media/steps/attack_%s.xlsx" % step["attack_id"])
            tests.append(results)

            #break
        tests = pd.concat(tests)
        tests.to_excel("./media/attack.xlsx")

    def test_decipher(self):
        for i, challenge in enumerate(challenges):
            print('')
            print("=" * 80)
            print(i)
            print(challenge["cipher_text"])
            print(challenge["key"])
            text = breakers.VigenereGeneticAlgorithmBreaker.cipher_factory(key=challenge["key"]).decipher(challenge["cipher_text"])
            print(text)
            print("-" * 80)

