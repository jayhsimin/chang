{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "d353ec50",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Import required mods\n",
    "import os\n",
    "import pandas as pd\n",
    "from fuzzywuzzy import fuzz\n",
    "import scipy.stats\n",
    "import numpy as np\n",
    "from scipy.spatial.distance import hamming\n",
    "import Levenshtein as LV\n",
    "import Levenshtein\n",
    "import os.path\n",
    "import shutil\n",
    "import re\n",
    "import statistics\n",
    "from glob import glob\n",
    "# get file path\n",
    "cpath=input('imagefilepath')     \n",
    "file1 = glob(f'{cpath}/*.csv') \n",
    "for file in file1:\n",
    "    CK=[]\n",
    "    DK=[]\n",
    "    ss=[]\n",
    "    tt=[]\n",
    "    L_ratio=[]\n",
    "    L_distance=[]\n",
    "    H_distance=[]\n",
    "    W_Distance=[]\n",
    "    W_Distance_Chang=[]\n",
    "    A_ratio=[]\n",
    "    A_partial_ratio=[]\n",
    "    D_distance=[]\n",
    "    K1_distance=[]\n",
    "    K2_distance=[]\n",
    "    K3_distance=[]\n",
    "    K4_distance=[]\n",
    "    K5_distance=[]\n",
    "    K6_distance=[]\n",
    "    K7_distance=[]\n",
    "    K8_distance=[]\n",
    "    K9_distance=[]    \n",
    "    df=pd.read_csv(file)#read CSV\n",
    "# Get image sorting results\n",
    "    for i in range(df.shape[0]):\n",
    "        CC=re.findall(r\"\\d+\",df['x34_rank'][i])\n",
    "        DD=re.findall(r'\\d+',df['t_rank'][i])\n",
    "        CK.append(CC)\n",
    "        DK.append(DD)\n",
    "        basenamess = os.path.basename(file)\n",
    "        bks = os.path.splitext(basenamess)[0]\n",
    "# The class that converts the sorting result into a module operation\n",
    "    df['x34']=CK\n",
    "    df['t']=DK\n",
    "    for s in CK:\n",
    "        results = list(map(int, s))\n",
    "        ss.append(results)\n",
    "    for t in DK:\n",
    "        results = list(map(int, t))\n",
    "        tt.append(results)\n",
    "    df['AAA']=ss\n",
    "    df['BBB']=tt\n",
    "    for n in range(df.shape[0]):      \n",
    "        GG=tuple(ss[n])\n",
    "        GF=tuple(tt[n])\n",
    "        D1=[str(GG)]\n",
    "        D2=[str(GF)]\n",
    "        # levenshtein Distance\n",
    "        ratio = Levenshtein.ratio(GG,GF)\n",
    "        dist = Levenshtein.distance(GG,GF)\n",
    "        L_ratio.append(ratio)\n",
    "        L_distance.append(dist)\n",
    "\n",
    "\n",
    "        # Hamming Distance\n",
    "        hamming_distance = hamming(GG, GF)*len(GG)\n",
    "        H_distance.append(hamming_distance)\n",
    "\n",
    "        #Wasserstein Distance\n",
    "        P = np.array(GG)\n",
    "        Q = np.array(GF)\n",
    "\n",
    "        dists=[i for i in range(len(P))]\n",
    "        Wasserstein_Distance=scipy.stats.wasserstein_distance(dists,dists,P,Q)\n",
    "        W_Distance.append(dist)\n",
    "\n",
    "        #Variation Wasserstein Distance *\n",
    "        c=tuple(abs(GG[i]-GF[i]) for i in range (0,len(GG)))\n",
    "        l=0\n",
    "        if range(len(c))==range(0, 4): \n",
    "            for discrepancy in c:\n",
    "                if discrepancy in range(0,1):\n",
    "                    l=l+discrepancy*1\n",
    "                if discrepancy in range(1,3):\n",
    "                    l=l+discrepancy*1\n",
    "                if discrepancy in range(3,5):\n",
    "                    l=l+discrepancy*2\n",
    "            W_Distance_Chang.append(l)\n",
    "        if range(len(c))==range(0, 8):\n",
    "            for discrepancy in c:\n",
    "                if discrepancy in range(0,3):\n",
    "                    l=l+discrepancy*2\n",
    "                if discrepancy in range(3,5):\n",
    "                    l=l+discrepancy*2\n",
    "                if discrepancy in range(5,9):\n",
    "                    l=l+discrepancy*3\n",
    "            W_Distance_Chang.append(l)\n",
    "        if range(len(c))==range(0, 12):\n",
    "            for discrepancy in c:\n",
    "                # print(discrepancy)\n",
    "                if discrepancy in range(0,4):\n",
    "                    l=l+discrepancy*3\n",
    "                if discrepancy in range(4,8):\n",
    "                    l=l+discrepancy*3\n",
    "                if discrepancy in range(8,12):\n",
    "                    l=l+discrepancy*5\n",
    "            W_Distance_Chang.append(l)\n",
    "\n",
    "        # Approximate string Distance\n",
    "        Approximate_string_distance = fuzz.ratio(GG,GF)\n",
    "        partial_ratio = fuzz.partial_ratio(GG,GF)   \n",
    "        A_ratio.append(Approximate_string_distance)\n",
    "        A_partial_ratio.append(partial_ratio)\n",
    "\n",
    "        # Dice coefficient distance        \n",
    "        c=bigram_sequence(D1)\n",
    "        d=bigram_sequence(D2) \n",
    "        Dice=dice(c, d)\n",
    "        D_distance.append(Dice)\n",
    "\n",
    "    df['L_ratio']=L_ratio\n",
    "    df['L_distance']=L_distance\n",
    "    df['H_distance']=H_distance\n",
    "    df['W_Distance']=W_Distance\n",
    "    df['W_Distance_Chang']=W_Distance_Chang\n",
    "    df['A_ratio']=A_ratio\n",
    "    df['A_partial_ratio']=A_partial_ratio\n",
    "    df['D_distance']=D_distance\n",
    "    aa=df.drop(columns=['x34_rank','t_rank','x34','t'])\n",
    "    \n",
    "    aa.to_csv(f'{fin}\\{bks}_a.csv',index=False)"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "aa",
   "language": "python",
   "name": "a"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.16"
  },
  "vscode": {
   "interpreter": {
    "hash": "acb835814e5ba3c48c53a7a641d99862593e2ec661bbff340dbbf7fcf06aa957"
   }
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
