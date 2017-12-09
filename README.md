# elevator <br />

##Thread跟Lock <br />
    Thread的start()被呼叫後會被活化(想不到其他詞QQ) <br />
    每個活化中的Thread會同時執行 <br />
    Thread被活化後會執行run()，run()裡面寫while，就能讓此thread一直不間斷執行 <br />
 <br />
    但有個東西能使Thread暫停，叫做Lock；可以把Lock想成一個資源，別想成一個鎖 <br />
    當這個資源被某個Thread給acquire()，代表該Thread佔據了這個資源 <br />
    當某個Thread將他佔據的資源給release()，代表此資源恢復自由 <br />
    當一個Thread試圖acquire()一個被占據的資源時，此Thread就會卡在該行程式碼；直到該資源恢復自由，此Thread會占據它並繼續執行 <br />
    有點像是Thread們排隊acquire該資源，前一個Thread將資源release，下一個Thread才能acquire()， <br />
    並且進入排隊中的Thread會卡住，直到排到他 <br />
 <br />
    以上是我的理解，不一定完全正確>< <br />
 <br />
