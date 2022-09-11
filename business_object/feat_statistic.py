from utils.singleton import Singleton
from dao.feat_dao import FeatDao
import pandas as pd


class FeatStatistic(metaclass=Singleton):
    def feat_count(self):           
        feat_dao = FeatDao()
          
        df_primary = pd.DataFrame(feat_dao.count_primary_artist(),
                                columns=['name', 'primary_count'])

        df_featured = pd.DataFrame(feat_dao.count_featured_artist(),
                                columns=['name', 'featured_count'])
        
        df_count = pd.merge(df_primary, df_featured,
                            on='name',how='outer').fillna(0)
        df_count['feat_count'] = df_count[['primary_count','featured_count']
                                        ].sum(axis=1).astype(int)
        df_count.drop(columns =['primary_count', 'featured_count'], inplace=True)

        return df_count.to_json(orient="records")
    
    def feat_mean(self):
        feat_dao = FeatDao()
    
        df_mean_feat = pd.DataFrame(feat_dao.date_count(),
                                 columns=['date', 'date_count'])
    
        df_mean_feat['mean'] = df_mean_feat['date_count'].rolling(3).mean()
        df_mean_feat.drop(columns=['date_count'], inplace=True)
        
        return df_mean_feat.to_json(orient='records')
