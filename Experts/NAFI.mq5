//+------------------------------------------------------------------+
//|                                                         NAFI.mq5 |
//|                                Copyright 2019, Ricardo Lourenço. |
//|                                       https://www.neoricalex.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2019, Ricardo Lourenço."
#property link      "https://www.neoricalex.com"
#property version   "0.1"
#property description "...."
#include <neoricalex/inicio.mqh>
//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit()
{
//---
    EventSetMillisecondTimer(MILLISECOND_TIMER);     // Set Millisecond Timer to get client socket input
    Print("[NEORICALEX]: Fazendo o Binding do Server <-> Socket na Porta " + IntegerToString(REP_PORT) + "..");
    repSocket.bind(StringFormat("%s://%s:%d", ZEROMQ_PROTOCOL, HOSTNAME, REP_PORT));
    /*
        Maximum amount of time in milliseconds that the thread will try to send messages 
        after its socket has been closed (the default value of -1 means to linger forever):
    */
    repSocket.setLinger(1000);  // 1000 milliseconds
    /* 
      If we initiate socket.send() without having a corresponding socket draining the queue, 
      we'll eat up memory as the socket just keeps enqueueing messages.    
      So how many messages do we want ZeroMQ to buffer in RAM before blocking the socket?
    */
    repSocket.setSendHighWaterMark(5);     // 5 messages only.
  //--- set MagicNumber for your orders identification
    int MagicNumber=123456;
    trade.SetExpertMagicNumber(MagicNumber);
  //--- set available slippage in points when buying/selling
    int deviation=10;
    trade.SetDeviationInPoints(deviation);
  //--- order execution mode
    trade.SetTypeFilling(ORDER_FILLING_RETURN);
  //--- logging mode: it would be better not to declare this method at all, the class will set the best mode on its own
    trade.LogLevel(1);
  //--- what function is to be used for trading: true - OrderSendAsync(), false - OrderSend()
    trade.SetAsyncMode(false);
  //---
    return(INIT_SUCCEEDED);
}
//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
{
    Print("[NEORICALEX]: Removendo o binding do Server <-> Socket na Porta " + IntegerToString(REP_PORT) + "..");
    repSocket.unbind(StringFormat("%s://%s:%d", ZEROMQ_PROTOCOL, HOSTNAME, REP_PORT));
}
//+------------------------------------------------------------------+
//| Expert timer function                                            |
//+------------------------------------------------------------------+
void OnTimer()
{   
    // Get client's response, but don't wait.
    repSocket.recv(request,true);
    // MessageHandler() should go here.   
    MessageHandler(request);
}
//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
  {
//---
   
  }
//+------------------------------------------------------------------+
//| Trade function                                                   |
//+------------------------------------------------------------------+
void OnTrade()
  {
  }
//+------------------------------------------------------------------+
//| TradeTransaction function                                        |
//+------------------------------------------------------------------+
void OnTradeTransaction(const MqlTradeTransaction& trans,
                        const MqlTradeRequest& request,
                        const MqlTradeResult& result)
  {
//---
   
  }
//+------------------------------------------------------------------+
//| ChartEvent function                                              |
//+------------------------------------------------------------------+
void OnChartEvent(const int id,
                  const long &lparam,
                  const double &dparam,
                  const string &sparam)
  {
//---
   
  }
//+------------------------------------------------------------------+
//| BookEvent function                                               |
//+------------------------------------------------------------------+
void OnBookEvent(const string &symbol)
  {
//---
   
  }
//+------------------------------------------------------------------+
