.class public Lcom/hcmusctf/androidrev/MainActivity;
.super Landroidx/appcompat/app/AppCompatActivity;
.source "MainActivity.java"


# instance fields
.field mResultWidget:Landroid/widget/TextView;


# direct methods
.method public constructor <init>()V
    .locals 1

    .line 14
    invoke-direct {p0}, Landroidx/appcompat/app/AppCompatActivity;-><init>()V

    .line 16
    const/4 v0, 0x0

    iput-object v0, p0, Lcom/hcmusctf/androidrev/MainActivity;->mResultWidget:Landroid/widget/TextView;

    return-void
.end method


# virtual methods
.method protected onCreate(Landroid/os/Bundle;)V
    .locals 4
    .param p1, "savedInstanceState"    # Landroid/os/Bundle;

    .line 20
    invoke-super {p0, p1}, Landroidx/appcompat/app/AppCompatActivity;->onCreate(Landroid/os/Bundle;)V

    .line 21
    const v0, 0x7f0a001c

    invoke-virtual {p0, v0}, Lcom/hcmusctf/androidrev/MainActivity;->setContentView(I)V

    .line 22
    const v0, 0x7f070078

    invoke-virtual {p0, v0}, Lcom/hcmusctf/androidrev/MainActivity;->findViewById(I)Landroid/view/View;

    move-result-object v0

    check-cast v0, Landroid/widget/EditText;

    .line 23
    .local v0, "flagWidget":Landroid/widget/EditText;
    const v1, 0x7f0700af

    invoke-virtual {p0, v1}, Lcom/hcmusctf/androidrev/MainActivity;->findViewById(I)Landroid/view/View;

    move-result-object v1

    check-cast v1, Landroid/widget/TextView;

    .line 24
    .local v1, "resultWidget":Landroid/widget/TextView;
    iput-object v1, p0, Lcom/hcmusctf/androidrev/MainActivity;->mResultWidget:Landroid/widget/TextView;

    .line 25
    new-instance v2, Lcom/hcmusctf/androidrev/MainActivity$1;

    invoke-direct {v2, p0}, Lcom/hcmusctf/androidrev/MainActivity$1;-><init>(Lcom/hcmusctf/androidrev/MainActivity;)V

    invoke-virtual {v0, v2}, Landroid/widget/EditText;->addTextChangedListener(Landroid/text/TextWatcher;)V

    .line 36
    const v2, 0x7f070058

    invoke-virtual {p0, v2}, Lcom/hcmusctf/androidrev/MainActivity;->findViewById(I)Landroid/view/View;

    move-result-object v2

    check-cast v2, Landroid/widget/Button;

    new-instance v3, Lcom/hcmusctf/androidrev/MainActivity$2;

    invoke-direct {v3, p0, v0, v1}, Lcom/hcmusctf/androidrev/MainActivity$2;-><init>(Lcom/hcmusctf/androidrev/MainActivity;Landroid/widget/EditText;Landroid/widget/TextView;)V

    invoke-virtual {v2, v3}, Landroid/widget/Button;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 51
    return-void
.end method
