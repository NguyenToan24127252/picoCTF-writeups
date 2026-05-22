.class Lcom/hcmusctf/androidrev/MainActivity$2;
.super Ljava/lang/Object;
.source "MainActivity.java"

# interfaces
.implements Landroid/view/View$OnClickListener;


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

.field final synthetic val$flagWidget:Landroid/widget/EditText;

.field final synthetic val$resultWidget:Landroid/widget/TextView;


# direct methods
.method constructor <init>(Lcom/hcmusctf/androidrev/MainActivity;Landroid/widget/EditText;Landroid/widget/TextView;)V
    .locals 0
    .param p1, "this$0"    # Lcom/hcmusctf/androidrev/MainActivity;

    .line 36
    iput-object p1, p0, Lcom/hcmusctf/androidrev/MainActivity$2;->this$0:Lcom/hcmusctf/androidrev/MainActivity;

    iput-object p2, p0, Lcom/hcmusctf/androidrev/MainActivity$2;->val$flagWidget:Landroid/widget/EditText;

    iput-object p3, p0, Lcom/hcmusctf/androidrev/MainActivity$2;->val$resultWidget:Landroid/widget/TextView;

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method


# virtual methods
.method public onClick(Landroid/view/View;)V
    .locals 3
    .param p1, "v"    # Landroid/view/View;

    .line 40
    iget-object v0, p0, Lcom/hcmusctf/androidrev/MainActivity$2;->this$0:Lcom/hcmusctf/androidrev/MainActivity;

    iget-object v1, p0, Lcom/hcmusctf/androidrev/MainActivity$2;->val$flagWidget:Landroid/widget/EditText;

    invoke-virtual {v1}, Landroid/widget/EditText;->getText()Landroid/text/Editable;

    move-result-object v1

    invoke-virtual {v1}, Ljava/lang/Object;->toString()Ljava/lang/String;

    move-result-object v1

    invoke-static {v0, v1}, Lcom/hcmusctf/androidrev/FlagChecker;->checkFlag(Landroid/content/Context;Ljava/lang/String;)Z

    move-result v0

    if-eqz v0, :cond_0

    .line 41
    const-string v0, "Valid flag!"

    .line 42
    .local v0, "msg":Ljava/lang/String;
    iget-object v1, p0, Lcom/hcmusctf/androidrev/MainActivity$2;->this$0:Lcom/hcmusctf/androidrev/MainActivity;

    invoke-virtual {v1}, Lcom/hcmusctf/androidrev/MainActivity;->getApplicationContext()Landroid/content/Context;

    move-result-object v1

    invoke-virtual {v1}, Landroid/content/Context;->getResources()Landroid/content/res/Resources;

    move-result-object v1

    const v2, 0x7f040034

    invoke-virtual {v1, v2}, Landroid/content/res/Resources;->getColor(I)I

    move-result v1

    .local v1, "color":I
    goto :goto_0

    .line 44
    .end local v0    # "msg":Ljava/lang/String;
    .end local v1    # "color":I
    :cond_0
    const-string v0, "Invalid flag"

    .line 45
    .restart local v0    # "msg":Ljava/lang/String;
    const/high16 v1, -0x10000

    .line 47
    .restart local v1    # "color":I
    :goto_0
    iget-object v2, p0, Lcom/hcmusctf/androidrev/MainActivity$2;->val$resultWidget:Landroid/widget/TextView;

    invoke-virtual {v2, v0}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 48
    iget-object v2, p0, Lcom/hcmusctf/androidrev/MainActivity$2;->val$resultWidget:Landroid/widget/TextView;

    invoke-virtual {v2, v1}, Landroid/widget/TextView;->setTextColor(I)V

    .line 49
    return-void
.end method
