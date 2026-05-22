.class Lcom/hcmusctf/androidrev/MainActivity$1;
.super Ljava/lang/Object;
.source "MainActivity.java"

# interfaces
.implements Landroid/text/TextWatcher;


# annotations
.annotation system Ldalvik/annotation/EnclosingMethod;
    value = Lcom/hcmusctf/androidrev/MainActivity;->onCreate(Landroid/os/Bundle;)V
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x0
    name = null
.end annotation


# instance fields
.field final synthetic this$0:Lcom/hcmusctf/androidrev/MainActivity;


# direct methods
.method constructor <init>(Lcom/hcmusctf/androidrev/MainActivity;)V
    .locals 0
    .param p1, "this$0"    # Lcom/hcmusctf/androidrev/MainActivity;

    .line 25
    iput-object p1, p0, Lcom/hcmusctf/androidrev/MainActivity$1;->this$0:Lcom/hcmusctf/androidrev/MainActivity;

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method


# virtual methods
.method public afterTextChanged(Landroid/text/Editable;)V
    .locals 0
    .param p1, "s"    # Landroid/text/Editable;

    .line 34
    return-void
.end method

.method public beforeTextChanged(Ljava/lang/CharSequence;III)V
    .locals 0
    .param p1, "s"    # Ljava/lang/CharSequence;
    .param p2, "start"    # I
    .param p3, "count"    # I
    .param p4, "after"    # I

    .line 27
    return-void
.end method

.method public onTextChanged(Ljava/lang/CharSequence;III)V
    .locals 2
    .param p1, "s"    # Ljava/lang/CharSequence;
    .param p2, "start"    # I
    .param p3, "before"    # I
    .param p4, "count"    # I

    .line 30
    iget-object v0, p0, Lcom/hcmusctf/androidrev/MainActivity$1;->this$0:Lcom/hcmusctf/androidrev/MainActivity;

    iget-object v0, v0, Lcom/hcmusctf/androidrev/MainActivity;->mResultWidget:Landroid/widget/TextView;

    const-string v1, ""

    invoke-virtual {v0, v1}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 31
    return-void
.end method
