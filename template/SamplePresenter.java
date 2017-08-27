package com.etiantian.dywteacher.ui.{page};

import com.etiantian.dywteacher.entity.{Bean};
import com.etiantian.dywteacher.mvpframe.exception.RxFunc;
import com.etiantian.dywteacher.mvpframe.rx.FilterSubscriber;

/**
 * auto-generate
 * by zwx
 */
public class {alias}Presenter extends {alias}Contract.Presenter {

    @Override
    void {apiName}({TypedParams}) {
        mRxManager.add(mModel.{apiName}({params})
                .map(new RxFunc.ServerResultFunc<{Bean}>())
                .onErrorResumeNext(new RxFunc.HttpResultFunc<{Bean}>())
                .subscribe(new FilterSubscriber<{Bean}>(mView) {

                    @Override
                    public void onNext({Bean} data) {
                        mView.on{ApiName}Success(data);
                    }
                }));
    }

}