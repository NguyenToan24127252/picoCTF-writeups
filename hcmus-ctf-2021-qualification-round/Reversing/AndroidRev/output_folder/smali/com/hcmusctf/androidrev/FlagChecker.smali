.class public Lcom/hcmusctf/androidrev/FlagChecker;
.super Ljava/lang/Object;
.source "FlagChecker.java"


# direct methods
.method public constructor <init>()V
    .locals 0

    .line 12
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method

.method private static bam(Ljava/lang/String;)Z
    .locals 1
    .param p0, "s"    # Ljava/lang/String;

    .line 59
    const-string v0, "^[0-9]+$"

    invoke-virtual {p0, v0}, Ljava/lang/String;->matches(Ljava/lang/String;)Z

    move-result v0

    return v0
.end method

.method private static bim(Ljava/lang/String;)Z
    .locals 1
    .param p0, "s"    # Ljava/lang/String;

    .line 51
    const-string v0, "^[a-z]+$"

    invoke-virtual {p0, v0}, Ljava/lang/String;->matches(Ljava/lang/String;)Z

    move-result v0

    return v0
.end method

.method private static bum(Ljava/lang/String;)Z
    .locals 1
    .param p0, "s"    # Ljava/lang/String;

    .line 55
    const-string v0, "^[A-Z]+$"

    invoke-virtual {p0, v0}, Ljava/lang/String;->matches(Ljava/lang/String;)Z

    move-result v0

    return v0
.end method

.method public static checkFlag(Landroid/content/Context;Ljava/lang/String;)Z
    .locals 12
    .param p0, "ctx"    # Landroid/content/Context;
    .param p1, "flag"    # Ljava/lang/String;

    .line 14
    const-string v0, "HCMUS-CTF{"

    invoke-virtual {p1, v0}, Ljava/lang/String;->startsWith(Ljava/lang/String;)Z

    move-result v0

    const/4 v1, 0x0

    if-eqz v0, :cond_7

    const-string v0, "}"

    invoke-virtual {p1, v0}, Ljava/lang/String;->endsWith(Ljava/lang/String;)Z

    move-result v0

    if-nez v0, :cond_0

    goto/16 :goto_3

    .line 18
    :cond_0
    const/16 v0, 0xa

    const/16 v2, 0x2a

    invoke-virtual {p1, v0, v2}, Ljava/lang/String;->substring(II)Ljava/lang/String;

    move-result-object v0

    .line 19
    .local v0, "core":Ljava/lang/String;
    invoke-virtual {v0}, Ljava/lang/String;->length()I

    move-result v2

    const/16 v3, 0x20

    if-eq v2, v3, :cond_1

    .line 20
    return v1

    .line 23
    :cond_1
    invoke-static {}, Lcom/hcmusctf/androidrev/FlagChecker;->foo()Ljava/lang/String;

    move-result-object v2

    invoke-virtual {v0, v2}, Ljava/lang/String;->split(Ljava/lang/String;)[Ljava/lang/String;

    move-result-object v2

    .line 24
    .local v2, "ps":[Ljava/lang/String;
    array-length v3, v2

    const/4 v4, 0x5

    if-ne v3, v4, :cond_6

    aget-object v3, v2, v1

    invoke-static {v3}, Lcom/hcmusctf/androidrev/FlagChecker;->bim(Ljava/lang/String;)Z

    move-result v3

    if-eqz v3, :cond_6

    const/4 v3, 0x2

    aget-object v4, v2, v3

    invoke-static {v4}, Lcom/hcmusctf/androidrev/FlagChecker;->bum(Ljava/lang/String;)Z

    move-result v4

    if-eqz v4, :cond_6

    const/4 v4, 0x4

    aget-object v5, v2, v4

    invoke-static {v5}, Lcom/hcmusctf/androidrev/FlagChecker;->bam(Ljava/lang/String;)Z

    move-result v5

    if-eqz v5, :cond_6

    const-string v5, "[A-Z]"

    const-string v6, "X"

    invoke-virtual {v0, v5, v6}, Ljava/lang/String;->replaceAll(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object v5

    const-string v6, "[a-z]"

    const-string v7, "x"

    invoke-virtual {v5, v6, v7}, Ljava/lang/String;->replaceAll(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object v5

    const-string v6, "[0-9]"

    const-string v7, " "

    invoke-virtual {v5, v6, v7}, Ljava/lang/String;->replaceAll(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object v5

    const-string v6, "[A-Za-z0-9]+.       .[A-Za-z0-9]+.[Xx ]+.[A-Za-z0-9 ]+"

    invoke-virtual {v5, v6}, Ljava/lang/String;->matches(Ljava/lang/String;)Z

    move-result v5

    if-nez v5, :cond_2

    goto/16 :goto_2

    .line 27
    :cond_2
    new-array v5, v4, [C

    .line 28
    .local v5, "syms":[C
    new-array v6, v4, [I

    fill-array-data v6, :array_0

    .line 29
    .local v6, "idxs":[I
    new-instance v7, Ljava/util/HashSet;

    invoke-direct {v7}, Ljava/util/HashSet;-><init>()V

    .line 30
    .local v7, "chars":Ljava/util/Set;, "Ljava/util/Set<Ljava/lang/Character;>;"
    const/4 v8, 0x0

    .local v8, "i":I
    :goto_0
    array-length v9, v5

    if-ge v8, v9, :cond_3

    .line 31
    aget v9, v6, v8

    invoke-virtual {p1, v9}, Ljava/lang/String;->charAt(I)C

    move-result v9

    aput-char v9, v5, v8

    .line 32
    aget-char v9, v5, v8

    invoke-static {v9}, Ljava/lang/Character;->valueOf(C)Ljava/lang/Character;

    move-result-object v9

    invoke-interface {v7, v9}, Ljava/util/Set;->add(Ljava/lang/Object;)Z

    .line 30
    add-int/lit8 v8, v8, 0x1

    goto :goto_0

    .line 34
    .end local v8    # "i":I
    :cond_3
    const/4 v8, 0x0

    .line 35
    .local v8, "sum":I
    array-length v9, v5

    const/4 v10, 0x0

    :goto_1
    if-ge v10, v9, :cond_4

    aget-char v11, v5, v10

    .line 36
    .local v11, "c":C
    add-int/2addr v8, v11

    .line 35
    .end local v11    # "c":C
    add-int/lit8 v10, v10, 0x1

    goto :goto_1

    .line 38
    :cond_4
    const/16 v9, 0xb4

    if-ne v8, v9, :cond_5

    invoke-interface {v7}, Ljava/util/Set;->size()I

    move-result v9

    const/4 v10, 0x1

    if-ne v9, v10, :cond_5

    const v9, 0x7f0c001c

    .line 39
    invoke-virtual {p0, v9}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    move-result-object v9

    const v11, 0x7f0c0022

    invoke-virtual {p0, v11}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    move-result-object v11

    invoke-static {v9, v11}, Lcom/hcmusctf/androidrev/FlagChecker;->gs(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object v9

    aget-object v11, v2, v1

    invoke-static {v9, v11}, Lcom/hcmusctf/androidrev/FlagChecker;->dh(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object v9

    const v11, 0x7f0c002b

    invoke-virtual {p0, v11}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    move-result-object v11

    invoke-static {p0, v9, v11}, Lcom/hcmusctf/androidrev/FlagChecker;->me(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;)Z

    move-result v9

    if-eqz v9, :cond_5

    const v9, 0x7f0c001d

    .line 40
    invoke-virtual {p0, v9}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    move-result-object v9

    const v11, 0x7f0c0023

    invoke-virtual {p0, v11}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    move-result-object v11

    invoke-static {v9, v11}, Lcom/hcmusctf/androidrev/FlagChecker;->gs(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object v9

    aget-object v11, v2, v10

    invoke-static {v9, v11}, Lcom/hcmusctf/androidrev/FlagChecker;->dh(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object v9

    const v11, 0x7f0c002c

    invoke-virtual {p0, v11}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    move-result-object v11

    invoke-static {p0, v9, v11}, Lcom/hcmusctf/androidrev/FlagChecker;->me(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;)Z

    move-result v9

    if-eqz v9, :cond_5

    const v9, 0x7f0c001e

    .line 41
    invoke-virtual {p0, v9}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    move-result-object v9

    const v11, 0x7f0c0024

    invoke-virtual {p0, v11}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    move-result-object v11

    invoke-static {v9, v11}, Lcom/hcmusctf/androidrev/FlagChecker;->gs(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object v9

    aget-object v3, v2, v3

    invoke-static {v9, v3}, Lcom/hcmusctf/androidrev/FlagChecker;->dh(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object v3

    const v9, 0x7f0c002d

    invoke-virtual {p0, v9}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    move-result-object v9

    invoke-static {p0, v3, v9}, Lcom/hcmusctf/androidrev/FlagChecker;->me(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;)Z

    move-result v3

    if-eqz v3, :cond_5

    const v3, 0x7f0c001f

    .line 42
    invoke-virtual {p0, v3}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    move-result-object v3

    const v9, 0x7f0c0025

    invoke-virtual {p0, v9}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    move-result-object v9

    invoke-static {v3, v9}, Lcom/hcmusctf/androidrev/FlagChecker;->gs(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object v3

    const/4 v9, 0x3

    aget-object v9, v2, v9

    invoke-static {v3, v9}, Lcom/hcmusctf/androidrev/FlagChecker;->dh(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object v3

    const v9, 0x7f0c002e

    invoke-virtual {p0, v9}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    move-result-object v9

    invoke-static {p0, v3, v9}, Lcom/hcmusctf/androidrev/FlagChecker;->me(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;)Z

    move-result v3

    if-eqz v3, :cond_5

    const v3, 0x7f0c0020

    .line 43
    invoke-virtual {p0, v3}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    move-result-object v3

    const v9, 0x7f0c0026

    invoke-virtual {p0, v9}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    move-result-object v9

    invoke-static {v3, v9}, Lcom/hcmusctf/androidrev/FlagChecker;->gs(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object v3

    aget-object v4, v2, v4

    invoke-static {v3, v4}, Lcom/hcmusctf/androidrev/FlagChecker;->dh(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object v3

    const v4, 0x7f0c002f

    invoke-virtual {p0, v4}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    move-result-object v4

    invoke-static {p0, v3, v4}, Lcom/hcmusctf/androidrev/FlagChecker;->me(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;)Z

    move-result v3

    if-eqz v3, :cond_5

    const v3, 0x7f0c0021

    .line 44
    invoke-virtual {p0, v3}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    move-result-object v3

    const v4, 0x7f0c0027

    invoke-virtual {p0, v4}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    move-result-object v4

    invoke-static {v3, v4}, Lcom/hcmusctf/androidrev/FlagChecker;->gs(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object v3

    invoke-static {v3, p1}, Lcom/hcmusctf/androidrev/FlagChecker;->dh(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object v3

    const v4, 0x7f0c0030

    invoke-virtual {p0, v4}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    move-result-object v4

    invoke-static {p0, v3, v4}, Lcom/hcmusctf/androidrev/FlagChecker;->me(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;)Z

    move-result v3

    if-eqz v3, :cond_5

    .line 46
    return v10

    .line 48
    :cond_5
    return v1

    .line 25
    .end local v5    # "syms":[C
    .end local v6    # "idxs":[I
    .end local v7    # "chars":Ljava/util/Set;, "Ljava/util/Set<Ljava/lang/Character;>;"
    .end local v8    # "sum":I
    :cond_6
    :goto_2
    return v1

    .line 15
    .end local v0    # "core":Ljava/lang/String;
    .end local v2    # "ps":[Ljava/lang/String;
    :cond_7
    :goto_3
    return v1

    nop

    :array_0
    .array-data 4
        0xf
        0x17
        0x1d
        0x22
    .end array-data
.end method

.method private static dh(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;
    .locals 2
    .param p0, "hash"    # Ljava/lang/String;
    .param p1, "s"    # Ljava/lang/String;

    .line 64
    :try_start_0
    invoke-static {p0}, Ljava/security/MessageDigest;->getInstance(Ljava/lang/String;)Ljava/security/MessageDigest;

    move-result-object v0

    .line 65
    .local v0, "md":Ljava/security/MessageDigest;
    invoke-virtual {p1}, Ljava/lang/String;->getBytes()[B

    move-result-object v1

    invoke-virtual {v0, v1}, Ljava/security/MessageDigest;->update([B)V

    .line 66
    invoke-virtual {v0}, Ljava/security/MessageDigest;->digest()[B

    move-result-object v1

    invoke-static {v1}, Lcom/hcmusctf/androidrev/FlagChecker;->toHexString([B)Ljava/lang/String;

    move-result-object v1
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0

    return-object v1

    .line 67
    .end local v0    # "md":Ljava/security/MessageDigest;
    :catch_0
    move-exception v0

    .line 68
    .local v0, "e":Ljava/lang/Exception;
    const/4 v1, 0x0

    return-object v1
.end method

.method public static foo()Ljava/lang/String;
    .locals 4

    .line 85
    const-string v0, "Vm0wd2QyVkZNVWRYV0docFVtMVNWVmx0ZEhkVlZscDBUVlpPVmsxWGVIbFdiVFZyVm0xS1IyTkliRmRXTTFKTVZsVmFWMVpWTVVWaGVqQTk="

    .line 86
    .local v0, "s":Ljava/lang/String;
    const/4 v1, 0x0

    .local v1, "i":I
    :goto_0
    const/16 v2, 0xa

    if-ge v1, v2, :cond_0

    .line 87
    new-instance v2, Ljava/lang/String;

    const/4 v3, 0x0

    invoke-static {v0, v3}, Landroid/util/Base64;->decode(Ljava/lang/String;I)[B

    move-result-object v3

    invoke-direct {v2, v3}, Ljava/lang/String;-><init>([B)V

    move-object v0, v2

    .line 86
    add-int/lit8 v1, v1, 0x1

    goto :goto_0

    .line 89
    .end local v1    # "i":I
    :cond_0
    return-object v0
.end method

.method private static gs(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;
    .locals 5
    .param p0, "a"    # Ljava/lang/String;
    .param p1, "b"    # Ljava/lang/String;

    .line 93
    const-string v0, ""

    .line 94
    .local v0, "s":Ljava/lang/String;
    const/4 v1, 0x0

    .local v1, "i":I
    :goto_0
    invoke-virtual {p0}, Ljava/lang/String;->length()I

    move-result v2

    if-ge v1, v2, :cond_0

    .line 95
    new-instance v2, Ljava/lang/StringBuilder;

    invoke-direct {v2}, Ljava/lang/StringBuilder;-><init>()V

    invoke-virtual {v2, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {p0, v1}, Ljava/lang/String;->charAt(I)C

    move-result v3

    invoke-virtual {p1}, Ljava/lang/String;->length()I

    move-result v4

    rem-int v4, v1, v4

    invoke-virtual {p1, v4}, Ljava/lang/String;->charAt(I)C

    move-result v4

    xor-int/2addr v3, v4

    int-to-char v3, v3

    invoke-static {v3}, Ljava/lang/Character;->toString(C)Ljava/lang/String;

    move-result-object v3

    invoke-virtual {v2, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    .line 94
    add-int/lit8 v1, v1, 0x1

    goto :goto_0

    .line 97
    .end local v1    # "i":I
    :cond_0
    return-object v0
.end method

.method private static me(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;)Z
    .locals 6
    .param p0, "ctx"    # Landroid/content/Context;
    .param p1, "s1"    # Ljava/lang/String;
    .param p2, "s2"    # Ljava/lang/String;

    .line 102
    const/4 v0, 0x0

    :try_start_0
    invoke-virtual {p1}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    move-result-object v1

    const v2, 0x7f0c0028

    invoke-virtual {p0, v2}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    move-result-object v2

    invoke-static {v2}, Lcom/hcmusctf/androidrev/FlagChecker;->r(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v2

    const/4 v3, 0x1

    new-array v4, v3, [Ljava/lang/Class;

    const-class v5, Ljava/lang/Object;

    aput-object v5, v4, v0

    invoke-virtual {v1, v2, v4}, Ljava/lang/Class;->getMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v1

    new-array v2, v3, [Ljava/lang/Object;

    aput-object p2, v2, v0

    invoke-virtual {v1, p1, v2}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v1

    check-cast v1, Ljava/lang/Boolean;

    invoke-virtual {v1}, Ljava/lang/Boolean;->booleanValue()Z

    move-result v0
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0

    return v0

    .line 103
    :catch_0
    move-exception v1

    .line 104
    .local v1, "e":Ljava/lang/Exception;
    new-instance v2, Ljava/lang/StringBuilder;

    invoke-direct {v2}, Ljava/lang/StringBuilder;-><init>()V

    const-string v3, "Exception: "

    invoke-virtual {v2, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-static {v1}, Landroid/util/Log;->getStackTraceString(Ljava/lang/Throwable;)Ljava/lang/String;

    move-result-object v3

    invoke-virtual {v2, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v2

    const-string v3, "HCMUS-CTF"

    invoke-static {v3, v2}, Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;)I

    .line 105
    return v0
.end method

.method public static r(Ljava/lang/String;)Ljava/lang/String;
    .locals 1
    .param p0, "s"    # Ljava/lang/String;

    .line 110
    new-instance v0, Ljava/lang/StringBuffer;

    invoke-direct {v0, p0}, Ljava/lang/StringBuffer;-><init>(Ljava/lang/String;)V

    invoke-virtual {v0}, Ljava/lang/StringBuffer;->reverse()Ljava/lang/StringBuffer;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/StringBuffer;->toString()Ljava/lang/String;

    move-result-object v0

    return-object v0
.end method

.method private static toHexString([B)Ljava/lang/String;
    .locals 7
    .param p0, "bytes"    # [B

    .line 73
    new-instance v0, Ljava/lang/StringBuilder;

    invoke-direct {v0}, Ljava/lang/StringBuilder;-><init>()V

    .line 74
    .local v0, "hexString":Ljava/lang/StringBuilder;
    array-length v1, p0

    const/4 v2, 0x0

    :goto_0
    if-ge v2, v1, :cond_1

    aget-byte v3, p0, v2

    .line 75
    .local v3, "b":B
    and-int/lit16 v4, v3, 0xff

    invoke-static {v4}, Ljava/lang/Integer;->toHexString(I)Ljava/lang/String;

    move-result-object v4

    .line 76
    .local v4, "hex":Ljava/lang/String;
    invoke-virtual {v4}, Ljava/lang/String;->length()I

    move-result v5

    const/4 v6, 0x1

    if-ne v5, v6, :cond_0

    .line 77
    const/16 v5, 0x30

    invoke-virtual {v0, v5}, Ljava/lang/StringBuilder;->append(C)Ljava/lang/StringBuilder;

    .line 79
    :cond_0
    invoke-virtual {v0, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 74
    .end local v3    # "b":B
    .end local v4    # "hex":Ljava/lang/String;
    add-int/lit8 v2, v2, 0x1

    goto :goto_0

    .line 81
    :cond_1
    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v1

    return-object v1
.end method
