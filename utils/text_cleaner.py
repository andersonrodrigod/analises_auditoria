import re
import string
import nltk
from nltk.corpus import stopwords


nltk.download("stopwords")

stop_words = stopwords.words("portuguese")


extra_stop_words = """DE OU POR COM E UNILATERAL DO OARA SEM DA IMPLANTE PARA PROCEDIMENTOS TECNICA ORIENTADA QUALQUER PROGRAMA 24 MESES UMA MES COBRAR CORRESPONDENTE SEGMENTO SEGMENTAR TOTAL EM J DEDICADO PERIFERICO TC SESSAO ARTICULAR VIDEOARTROSCOPICOS US CORONARIA TRATAMENTO QUANDO VIA PERCUTANEA TERAPEUTICA DIAGNOSTICA VIDEOENDOSCOPIA RETIRADA CORONARIANA RESSECCAO QUIMIOTERAPICO ANTIANGIOGENICO RX CIRURGICO CIRURGICA VASO NERVO RM TURBINOPLASTIA ONCOLOGICO  INTRA CARTILAGINOSA VERTEBRAL A STENT TENDAO O DISCO CARDIACO PROCEDIMENTO BILATERAL FARMACOLOGICA TRANSLUMINAL 1 SISTEMA PROVAS COLOCACAO CIRURGIA CIRCUITO PARCIAL LIGAMENTO INCLUI RADIOFREQUENCIA BALAO SENSIBILIZACAO ARRITMOGENICO  VEIAS INTRODUCAO MULTIPOLAR NAS CODIGO VIDEOLAPAROSCOPIA LAPAROSCOPICA CATETER MAPEAMENTO SEPTOPLASTIA ENDOSCOPICA CORRECAO TUNEL OMBRO ADENOIDECTOMIA URETER RECONSTRUCAO REFORCO COXOFEMORAL ANESTESIA METODO FACETARIA PUNHO CARPO FACETAS RETENCIONAMENTO MULTIPLOS VASOS BIFURCACAO IMPACTO FEMORO ACETABULAR OPERATORIA INFUSAO INTRAVITREA MEDICAMENTO ANTI INFLAMATORIO ELETROANATOMICO TRIDIMENSIONAL AMBIENTE LABRAL ANTERIOR DRENAGEM NEVRALGIA ORIENTADO ARTICULARES HOSPITALAR IMAGEM SUTURA TRIGEMIO LOMBAR MONITORIZACAO LATERAL RECIDIVANTE CRUZADO TEMPORO TEMPORO ARTICULACAO NEUROFISIOLOGICA MANDIBULAR AO NIVEL GERADOR MENISCO REPARO TRANSPOSICAO VIDEOTORACOSCOPIA PLEUROSCOPIA VIDEO PLEURAL FECHADA ALTA C INSTRUMENTACAO NERVOSO SINEQUIAS UNICO FETO MULTIPLO IMPLANTES PERIDURAL SUBARACNOIDEO ESPLENECTOMIA CORTICOIDE APARELHO EXTENSOR REALINHAMENTOS POS CONTROLE CLAVICULA GERAL DOS DEDOS COXA FÊMUR ABDOME AVENTAL EXPLORADORA RETALHOS POSTERIOR LESOES CANAL ESTREITO CAUDA EQUINA MAIS LIGAMENTARES EXTERNA TUBO VENTILACAO CORPOS INSTALACAO DO CIRCUITO DE CIRCULACAO EXTRACORPOREA CONVENCIONAL PROGNATISMO MICROGNATISMO OPERACAO DE PROCESSADORA AUTOMATICA DE SANGUE EM AUTOTRANSFUSAO INTRA/OPERATORIA VERTEBROPLASTIA OUTRAS CXL COLAGENO CORNEANO PERFUSIONISTA CARDIACA E POR VIA  OVARIANAS VARICOCEL TRONCO VENOSO VASCULAR RETALHO COMPOSTO INCLUINDO CARTILAGEM OSSO VARICOCELE EXPLORACAO CIRURGICA DE NERVO ELETRODOS ESTIMULACAO CEREBRAL INTRAVASCULAR TRANSOPERATORIA POSICIONAMENTO NEUROLISE EXTERNA RADIOSCOPIA ACOMPANHAMENTO HORA FRACAO MICROCIRURGICO DISSECCAO VEIA NEUROLITICO CENTRAL AUTONOMO GALEA APONEUROTICA AVALIACAO FISIOLOGICA GRAVIDADE OBSTRUCOES GUIA INTERNA FLEXIVEL TIMPANO MASTOIDECTOMIA TRIANGULAR NARIZ ANIPULACAO SOB OUTROS PUNCOES MICROCIRURGIA TRANSESFENOIDAL ESTABILIZACAO PLASTIA CAVO COALISAO TARSAL LIQUORICA COCLEAR EXCETO PROTESE VERSAO INTRAVITREO POLIMERO FARMACOLOGICO LIBERACAO MANIPULACAO MENISCORRAFIA ANEURISMA OCLUSAO SACULAR CONCOMITANTE CORONARIO ETMOIDECTOMIA INTRANASAL ESTEREOTAXIA RESSECCAO ENXERTIA JOELHO URETEROSCOPICA DO SISTEMA DE CONDUCAO COM OU SEM ACAO FARMACOLOGICA HEMATOMA PANARICIO""".split()

custom_stop_words = set(stop_words + extra_stop_words)


def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = text.upper()
    text = re.sub(f"[{string.punctuation}]", " ", text)
    words = text.split()
    words = [w for w in words if w not in custom_stop_words]
    return " ".join(words)


def normalize_words(df, column="word"):

    def mapper(word):
        word_upper = word.upper()

        if "OCULAR" in word_upper:
            return "TRAT.OCULAR"
        if "DUPLO" in word_upper:
            return "PROCED.C/DUPLO_J"
        if "ESTUDO ELETROFISIOLOGICO" in word_upper:
            return "ESTUDO/ELETRO"
        if "OSTEOCONDROPLASTIA" in word_upper:
            return "OSTEOCONDRO"
        if "ESTUDO ELETROFISIOLOGICO" in word_upper:
            return "ESTUDO/ELETRO"
        if "ANOMALOS" in word_upper:
            return "MAP/ANOMALOS"
        if "LINFADENECTOMIA PELVICA" in word_upper:
            return "LINF/PELVICA"
        if "REIMPLANTE URETERAL EXTRAVESICAL" in word_upper:
            return "REIMP/URETAL"
        if "HEMODIALISE AMBULATORIAL" in word_upper:
            return "HEMODIALISE"
        if "TERAPIA IMUNOPROFILATICA" in word_upper:
            return "TER/IMUNO"
        if "POLIPECTOMIA" in word_upper:
            return "POLIPECTOMIA"
        if "VITRECTOMIA" in word_upper:
            return "VITRECTOMIA"
        if "MICRONEUROLISE" in word_upper:
            return "VITRECTOMIA"
        if "COLONOSCOPIA" in word_upper:
            return "VITRECTOMIA"
        if "HISTERECTOMIA" in word_upper:
            return "HISTERECTOMIA"
        if "GASTRECTOMIA" in word_upper:
            return "GASTRECTOMIA"
        if "RETINOPEXIA" in word_upper:
            return "RETINOPEXIA"
        if "PERCUTANEO ENDO" in word_upper:
            return "PER/ENDO"
        if "TUMOR OSSEO" in word_upper:
            return "TUMOR OSSEO"
        if "PAROTIDECTOMIA" in word_upper:
            return "PAROTIDECTOMIA"
        if "CATETERISMO" in word_upper:
            return "CATETERISMO"
        if "RUPTURA MANGUITO" in word_upper:
            return "MANG_ROTADOR"
        if "DOPPLER COLORIDO OPERATORIO" in word_upper:
            return "DOPPLER/COLOR"
        if "CISTO HEPATICO" in word_upper:
            return "RESEC/CISTO_HEP"
        if "LAQUEADURA" in word_upper:
            return "LAQUEADURA"
        if "ENUCLEACAO" in word_upper:
            return "ENUCLEACAO"
        if "COLECISTECTOMIA" in word_upper:
            return "COLECISTEC"
        if "URETERORRENOLITOTRIPSIA" in word_upper:
            return "URETERO"
        if "ARTRODESE TORNOZELO" in word_upper:
            return "ARTRODESE/TORNOZ"
        if "DESCOMPRESSAO MEDULAR" in word_upper:
            return "DECOMP/MEDUL"
        if "ENXERTO OSSEO" in word_upper:
            return "ENXERTO_OSSEO"
        if "TENOPLASTIA" in word_upper :
            return "TENOPLASTIA"
        if "PUNCAO TRANSEPTAL" in word_upper :
            return "PUNCAO/TRANS"
        if "PUNCAO BIOPSIA" in word_upper :
            return "BIOPSIA"
        if "TENOARTROPLASTIA" in word_upper :
            return "ARTROPLASTIA_B"
        if "ESTUDO ULTRA SONOGRAFICO" in word_upper:
            return "EST/ULT/SONO"
        if "CATETERIZACAO TRANSEPTAL" in word_upper:
            return "CAT/TRANS"
        
        if "EMBOLIZACAO" in word_upper or "MEDULAR" in word_upper:
            return "EMBOLIZACAO"
        
        




        if "HERNIA" in word_upper or "HERNIORRAFIA" in word_upper:
            return "HERNIA/HERNIO"
        if "AMIGDALECTOMIA" in word_upper or "ADENOIDECTOMIA" in word_upper:
            return "AMIGDAL/ADENOID"
        if "DEFINIR" in word_upper or "ADMINISTRATIVAMENTE" in word_upper:
            return "A_DEFINIR"
        if "IMPLANTE_DE_ANEL" in word_upper or "ANEL" in word_upper: 
            return "IMPLANTE_ANEL"
        if "PROCED" in word_upper or "PROCED._ODONTOLOGICO" in word_upper:
            return "PROCED.ODONTO"
        if "PRÓTESE" in word_upper or "MAMA" in word_upper:
            return "PRÓTESE_MAMA"
        if "MARCA" in word_upper or "PASSO" in word_upper:
            return "MARCA_PASSO"
        if "TROCA" in word_upper or "VALVAR" in word_upper:
            return "TROCA_VALVAR"
        if "PLASTICA" in word_upper or "EM_Z_OU_W" in word_upper:
            return "PLÁSTICA_PENIANA"
        if "REVASCULARIZACAO" in word_upper or "MIOCARDIO" in word_upper:
            return "REVAS.MIOCARD"
        if "OSTEOPLASTIAS MANDIBULA" in word_upper or "OSTEOPLASTIA DISCECTOMIA" in word_upper:
            return "OSTEO/BUCOMAX"    
        if "ARTROPLASTIA" in word_upper or "JOELHO" in word_upper:
            return "ARTROP/JOELHO"
        if "ARTROPLASTIA" in word_upper or "QUADRIL" in word_upper:
            return "ARTROP/QUADRIL"
        if "ARTROPLASTIA" in word_upper or "ESCAPULO UMERAL" in word_upper:
            return "ARTROP/ESC_UME"
        if "ARTROPLASTIA" in word_upper or "LUXACAO" in word_upper:
            return "ARTROP/LUXA"
        if "ARTROPLASTIA" in word_upper or "COTOVELO" in word_upper:
            return "ARTROP/COTO"
        if "CRONICAS" in word_upper or "MAO" in word_upper:
            return "LES/LIG_MAO"
        if "CRONICAS" in word_upper or "TORNOZELO" in word_upper:
            return "LES/LIG_TORNOZ"
        if "ANGIOTOMOGRAFIA" in word_upper or "TC ANGIOTOMOGRAFIA" in word_upper:
            return "ANGIOTOMOGRAFIA"
        
        

        if "CORPO ESTRANHO PAREDE TORACICA" in word_upper or "CORPO ESTRANHO SUBCUTANEO" in word_upper or "CORPO ESTRANHO EXTRACAO BEXIGA" in word_upper:
            return "RET/CORPO_EST"
        if "INFILTRACAO TECIDOS" in word_upper or "PUNCAO" in word_upper or "INFILTRACAO MEDICAMENTOSA" in word_upper:
            return "PUNCAO/INFILT."
        if "PSEUDARTROSES" in word_upper or "OSTEOTOMIAS" in word_upper and "BRACO" in word_upper:
            return "OSTEOT/BRAÇO"
        if "PSEUDARTROSES" in word_upper or "OSTEOTOMIAS" in word_upper and "TORNOZELO" in word_upper:
            return "OSTEOT/TORNOZ"
        if "OSTEOTOMIAS" in word_upper or "OSTEOTOMIAS" in word_upper and "ANTEBRAÇO" in word_upper:
            return "OSTEOT/ANTBRA"
        if "OSTEOTOMIAS" in word_upper or "OSTEOTOMIAS" in word_upper and "PERNA" in word_upper:
            return "OSTEOT/PERNA"
        if "OSTEOTOMIA" in word_upper or "OSTEOTOMIAS" in word_upper and "JOELHO" in word_upper:
            return "OSTEOT/JOELHO"
        if "OSTEOTOMIA" in word_upper or "OSTEOTOMIAS" in word_upper and "METATARSOS" in word_upper:
            return "OSTEOT/META"
        
        
        if "ABLACAO" in word_upper or"GATILHOS" in word_upper or "SUBSTRATOS" in word_upper or "ARRITMOGENICOS" in word_upper or "ELETROFISIOLOGICA" in word_upper:
            return "ABLACAO"
        if "COLUNA" in word_upper or "ARTRODESE COLUNA POSTERO" in word_upper or "ARTRODESE COLUNA" in word_upper or "PSEUDARTROSE COLUNA" in word_upper or "CIRURGIA DE COLUNA" in word_upper or "INFILTRACAO FORAMINAL" in word_upper:
            return "CIR/COLUNA"
        

        
        # Adicione outros agrupamentos aqui se quiser
        return word

    df[column] = df[column].apply(mapper)
    return df


