
//-- Incluir as bibliotecas para fazer o Trade
#include <Trade/Trade.mqh>
#include <Trade\SymbolInfo.mqh>
//-- Instancia as classes
CTrade trade; // Classe responsável pela execução de trades
CSymbolInfo info_ticker;
//--- Iniciar o ZMQ
#include <Zmq\zmq.mqh>
extern string PROJECT_NAME = "TradeServer";
extern string ZEROMQ_PROTOCOL = "tcp";
extern string HOSTNAME = "*";
extern int REP_PORT = 5555;
extern int MILLISECOND_TIMER = 1;  // 1 millisecond
extern string t0 = "--- Trading Parameters ---";
//extern int MagicNumber =25388904;
Context context(PROJECT_NAME);
Socket repSocket(context,ZMQ_REP);
uchar myData[];
ZmqMsg request;
//+------------------------------------------------------------------+
//| ZMQ Message Handler                                              |
//+------------------------------------------------------------------+
void MessageHandler(ZmqMsg &localRequest)
{
    // Output object
    ZmqMsg reply; 
    // Message components for later.
    string components[];
    if(localRequest.size() > 0) {
        // Get data from request   
        ArrayResize(myData, localRequest.size());
        localRequest.getData(myData);
        string dataStr = CharArrayToString(myData);
        // Process data
        ParseZmqMessage(dataStr, components);
        // Interpret data
        InterpretZmqMessage(components);
    }
}
//+------------------------------------------------------------------+
void ParseZmqMessage(string& message, string& retArray[]) 
{   
    Print("Parseando: " + message);
    string sep = "|";
    ushort u_sep = StringGetCharacter(sep,0);
    int splits = StringSplit(message, u_sep, retArray);
    for(int i = 0; i < splits; i++) {
        Print(IntegerToString(i) + ") " + retArray[i]);
    }
}
//+------------------------------------------------------------------+
ENUM_TIMEFRAMES TFMigrate(int tf)
{
    switch(tf)
    {
        case 0: return(PERIOD_CURRENT);
        case 1: return(PERIOD_M1);
        case 5: return(PERIOD_M5);
        case 15: return(PERIOD_M15);
        case 30: return(PERIOD_M30);
        case 60: return(PERIOD_H1);
        case 240: return(PERIOD_H4);
        case 1440: return(PERIOD_D1);
        case 10080: return(PERIOD_W1);
        case 43200: return(PERIOD_MN1);
        
        case 2: return(PERIOD_M2);
        case 3: return(PERIOD_M3);
        case 4: return(PERIOD_M4);      
        case 6: return(PERIOD_M6);
        case 10: return(PERIOD_M10);
        case 12: return(PERIOD_M12);
        case 16385: return(PERIOD_H1);
        case 16386: return(PERIOD_H2);
        case 16387: return(PERIOD_H3);
        case 16388: return(PERIOD_H4);
        case 16390: return(PERIOD_H6);
        case 16392: return(PERIOD_H8);
        case 16396: return(PERIOD_H12);
        case 16408: return(PERIOD_D1);
        case 32769: return(PERIOD_W1);
        case 49153: return(PERIOD_MN1);      
        default: return(PERIOD_CURRENT);
    }
}

//+------------------------------------------------------------------+
// Interpret Zmq Message and perform actions
void InterpretZmqMessage(string& compArray[])
{
    Print("[NEORICALEX]: Interpretando a mensagem..");
    int switch_action = 0;
    string volume;
    double lotes;
    int barra_shift; // Shift da Barra ou vela
  //--- number of decimal places
    int    digits=(int)SymbolInfoInteger(_Symbol,SYMBOL_DIGITS);
  //--- point value
    double point=SymbolInfoDouble(_Symbol,SYMBOL_POINT);
  //--- receiving a buy price
    double price=SymbolInfoDouble(_Symbol,SYMBOL_ASK);
  //--- calculate and normalize SL and TP levels
    double SL=NormalizeDouble(price-1000*point,digits);
    double TP=NormalizeDouble(price+1000*point,digits);
  //--- filling comments
    string comment="Buy "+_Symbol+lotes+" at "+DoubleToString(price,digits);
    if (compArray[0] == "COTACOES")
        switch_action = 1;
    else if (compArray[0] == "TRADE" && compArray[1] == "OPEN")
        switch_action = 2;
    else if (compArray[0] == "TRADE" && compArray[1] == "CLOSE")
        switch_action = 3;
    else if (compArray[0] == "DATA")
        switch_action = 4;
    else if (compArray[0] == "HISTORICO")
        switch_action = 5;
    else if (compArray[0] == "INFO_CONTA")
        switch_action = 6;
    else if (compArray[0] == "INFO_TICKER")
        switch_action = 7;
    string ret = "";
    int ticket;
    // https://www.mql5.com/pt/articles/138
    long max_vol;
    double ask;
    string ticker;
    bool ans = false;
    MqlRates rates[]; // Case DADOS
    MqlRates rate[]; // Case TESTE
    ArraySetAsSeries(rates, true);    
    int price_count = 0;
    ZmqMsg msg("[NEORICALEX]: Processando a mensagem...");
    switch(switch_action) 
    {
        case 1: 
            ret = "N/A"; 
            if(ArraySize(compArray) > 1) 
                ret = GetCurrent(compArray[1]);
            Print("Enviando: " + ret);
            repSocket.send(ret, false);
            break;
        case 2: 
            ret = "";
            lotes = compArray[2];
          //--- everything is ready, trying to open a buy position
            if(!trade.PositionOpen(_Symbol,ORDER_TYPE_BUY,lotes,price,SL,TP,comment))
              {
                //--- failure message
                Print("PositionOpen() method failed. Return code=",trade.ResultRetcode(),
                      ". Code description: ",trade.ResultRetcodeDescription());
              }
            else
              {
                Print("PositionOpen() method executed successfully. Return code=",trade.ResultRetcode(),
                      " (",trade.ResultRetcodeDescription(),")");
                ret = trade.ResultOrder();
              }
            Print("Enviando: " + ret);
            repSocket.send(ret, false);
            break;
        case 3:
            ret = "N/A";
            ticket = compArray[2];
          //--- closing a position at the current symbol
            if(!trade.PositionClose(ticket))
              {
                //--- failure message
                Print("PositionClose() method failed. Return code=",trade.ResultRetcode(),
                      ". Code description: ",trade.ResultRetcodeDescription());
              }
            else
              {
                Print("PositionClose() method executed successfully. Return code=",trade.ResultRetcode(),
                      " (",trade.ResultRetcodeDescription(),")");
              }
            repSocket.send(ret, false);
            break;
        case 4:
            ret = "";
            // Format: DATA|SYMBOL|TIMEFRAME|START_DATETIME|END_DATETIME
            price_count = CopyRates(compArray[1], TFMigrate(StringToInteger(compArray[2])),
                          StringToTime(compArray[3]), StringToTime(compArray[4]),
                          rates);
            
            if (price_count > 0)
            {              
                // Construct string of price|price|price|.. etc and send to PULL client.
                for(int i = 0; i < price_count; i++ ) {
                     ret = ret + StringFormat("%.6f,%.6f,%.6f,%.6f,%d,%d", rates[i].open, rates[i].high, rates[i].low, rates[i].close, rates[i].tick_volume, rates[i].real_volume);
                }
              
                Print("Enviando: " + ret);
                repSocket.send(ret, false);
            }
            break;
        case 5:
            barra_shift = compArray[1]; // numero de Barras anteriores
            ret = "";
            CopyRates(compArray[2],PERIOD_CURRENT,barra_shift,1,rate);
            Print("Enviando: O=",rate[0].open," C=",rate[0].close," Data: ", rate[0].time);
            ret = ret + StringFormat("%.6f,%.6f,%.d", rate[0].open, rate[0].close, rate[0].time);
            repSocket.send(ret, false);
            break;
        case 6:
            printf("ACCOUNT_BALANCE =  %G",AccountInfoDouble(ACCOUNT_BALANCE)); 
            printf("ACCOUNT_CREDIT =  %G",AccountInfoDouble(ACCOUNT_CREDIT)); 
            printf("ACCOUNT_PROFIT =  %G",AccountInfoDouble(ACCOUNT_PROFIT)); 
            printf("ACCOUNT_EQUITY =  %G",AccountInfoDouble(ACCOUNT_EQUITY)); 
            printf("ACCOUNT_MARGIN =  %G",AccountInfoDouble(ACCOUNT_MARGIN)); 
            printf("ACCOUNT_MARGIN_FREE =  %G",AccountInfoDouble(ACCOUNT_MARGIN_FREE)); 
            printf("ACCOUNT_MARGIN_LEVEL =  %G",AccountInfoDouble(ACCOUNT_MARGIN_LEVEL)); 
            printf("ACCOUNT_MARGIN_SO_CALL = %G",AccountInfoDouble(ACCOUNT_MARGIN_SO_CALL)); 
            printf("ACCOUNT_MARGIN_SO_SO = %G",AccountInfoDouble(ACCOUNT_MARGIN_SO_SO));
            ret = ret + StringFormat("%.2f,%G,%G,%.2f,%G,%.2f,%G,%G,%G, %.d", AccountInfoDouble(ACCOUNT_BALANCE),
                                      AccountInfoDouble(ACCOUNT_CREDIT), AccountInfoDouble(ACCOUNT_PROFIT),
                                      AccountInfoDouble(ACCOUNT_EQUITY), AccountInfoDouble(ACCOUNT_MARGIN),
                                      AccountInfoDouble(ACCOUNT_MARGIN_FREE), AccountInfoDouble(ACCOUNT_MARGIN_LEVEL),
                                      AccountInfoDouble(ACCOUNT_MARGIN_SO_CALL), AccountInfoDouble(ACCOUNT_MARGIN_SO_SO),
                                      TimeCurrent() );
            repSocket.send(ret, false);
            break;
        case 7: 
            ret = "N/A"; 
            if(ArraySize(compArray) > 1) 
                ret = GetCurrent(compArray[1]);
            Print("Enviando: " + ret);
            repSocket.send(ret, false);
            break;
        default: 
            break;
    }
}
//+------------------------------------------------------------------+
string GetVolume(string symbol, datetime start_time, datetime stop_time)
{
    long volume_array[1];
    CopyRealVolume(symbol, PERIOD_M1, start_time, stop_time, volume_array);
    return(StringFormat("%d", volume_array[0]));
}
//+------------------------------------------------------------------+
string GetCurrent(string symbol)
{
    MqlTick Last_tick;
    SymbolInfoTick(symbol,Last_tick);    
    double bid = Last_tick.bid;
    double ask = Last_tick.ask;
    MqlBookInfo bookArray[]; 
    bool getBook = MarketBookGet(symbol,bookArray);
    long buy_volume = 0;
    long sell_volume = 0;
    long buy_volume_market = 0;
    long sell_volume_market = 0;
    if (getBook) {
       for (int i =0; i < ArraySize(bookArray); i++ ) 
       {
            if (bookArray[i].type == BOOK_TYPE_SELL)
               sell_volume += bookArray[i].volume_real;
            else if (bookArray[i].type == BOOK_TYPE_BUY)
               buy_volume += bookArray[i].volume_real;
            else if (bookArray[i].type == BOOK_TYPE_BUY_MARKET)
               buy_volume_market += bookArray[i].volume_real;
            else
               sell_volume_market += bookArray[i].volume_real;
       }
    }
    long tick_volume = Last_tick.volume;
    long real_volume = Last_tick.volume_real;
    MarketBookAdd(symbol);
    return(StringFormat("%.6f,%.6f,%d,%d,%d,%d,%d,%d,%d", bid, ask, buy_volume, sell_volume, tick_volume, real_volume, buy_volume_market, sell_volume_market, TimeCurrent()));
}